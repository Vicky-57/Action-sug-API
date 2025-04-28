from django.db import models

class QueryLog(models.Model):
    """
    Model to log every API request, its analysis, and suggested actions.
    """
    query = models.TextField(help_text="The original user query text")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the query was received")
    tone = models.CharField(max_length=50, help_text="Identified tone from the analysis")
    intent = models.CharField(max_length=100, help_text="Identified intent from the analysis")
    suggested_actions = models.JSONField(help_text="List of suggested actions as JSON")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Query Log"
        verbose_name_plural = "Query Logs"
    
    def __str__(self):
        return f"{self.query[:30]}... ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"