from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_message_analysis
from .action_suggester import suggest_actions
from .models import QueryLog
from .serializers import QuerySerializer

class AnalyzeMessageView(APIView):
    """
    API endpoint that analyzes a text message and suggests relevant actions.
    """
    
    def post(self, request):
        """
        Process a POST request to analyze a message.
        """
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            query = serializer.validated_data['query']
            
            try:
                # Get tone and intent analysis
                analysis = get_message_analysis(query)
                
                suggested_actions = suggest_actions(analysis['tone'], analysis['intent'])
                
                # Prepare the response
                response_data = {
                    'query': query,
                    'analysis': analysis,
                    'suggested_actions': suggested_actions
                }
                
                # Log the query and response to the database
                QueryLog.objects.create(
                    query=query,
                    tone=analysis['tone'],
                    intent=analysis['intent'],
                    suggested_actions=suggested_actions
                )
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response(
                    {'error': f'Analysis failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)