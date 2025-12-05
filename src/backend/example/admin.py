# from django.contrib import admin
# from .models import AnalysisProject, DataFile, ModelConfiguration, AnalysisResult


# @admin.register(AnalysisProject)
# class AnalysisProjectAdmin(admin.ModelAdmin):
#     list_display = ['name', 'user', 'created_at', 'updated_at']
#     list_filter = ['created_at', 'updated_at']
#     search_fields = ['name', 'description']


# @admin.register(DataFile)
# class DataFileAdmin(admin.ModelAdmin):
#     list_display = ['original_filename', 'project', 'file_size', 'is_processed', 'uploaded_at']
#     list_filter = ['is_processed', 'uploaded_at']
#     search_fields = ['original_filename']


# @admin.register(ModelConfiguration)
# class ModelConfigurationAdmin(admin.ModelAdmin):
#     list_display = ['project', 'model_type', 'is_trained', 'created_at']
#     list_filter = ['model_type', 'is_trained', 'created_at']


# @admin.register(AnalysisResult)
# class AnalysisResultAdmin(admin.ModelAdmin):
#     list_display = ['model_config', 'created_at']
#     list_filter = ['created_at']