from rest_framework import serializers
from .models import Genre, Movie, Video, VideoRating, ReportVideo, ReportRating


class VideoFileSerializer(serializers.ModelSerializer):
    videoFile = serializers.FileField()  # For file uploads
    genre = serializers.ChoiceField(choices=Genre.choices)  # Dropdown for genre

    class Meta:
        model = Video
        fields = ['videoFile', 'genre', 'title', 'description','id']

    def validate_videoFile(self, value):
        # Validate file type
        allowed_extensions = ('.mp4', '.mov', '.avi')
        if not value.name.endswith(allowed_extensions):
            raise serializers.ValidationError(
                f"Invalid file format. Only {', '.join(allowed_extensions)} files are allowed."
            )
        
        # Validate file size
        max_file_size = 50 * 1024 * 1024  # 50 MB limit
        if value.size > max_file_size:
            raise serializers.ValidationError(
                "File size exceeds the 50MB limit."
            )
        
        return value

class VideoEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'genre']

class VideoRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRating
        fields = ['id','video', 'commentor', 'content', 'is_edited', 'date', 'pinned','rating']
        read_only_fields = ['commentor', 'date', 'pinned', 'is_edited']

    def validate_content(self, value):
        if len(value) > 600:
            raise serializers.ValidationError("Content must be 600 characters or less.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    def create(self, validated_data):
        validated_data['commentor'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.commentor != user:
            raise serializers.ValidationError("You can only edit your own ratings.")
        return super().update(instance, validated_data)

    def delete(self, instance):
        user = self.context['request'].user
        if instance.commentor != user:
            raise serializers.ValidationError("You can only delete your own ratings.")
        instance.delete()

class ReportVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportVideo
        fields = ['video', 'reason', 'video_reporter', 'date', 'resolved']
        read_only_fields = ['video_reporter', 'date']

    def create(self, validated_data):
        validated_data['video_reporter'] = self.context['request'].user
        return super().create(validated_data)


class ReportRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRating
        fields = ['comment', 'reason', 'rating_reporter', 'date', 'resolved']
        read_only_fields = ['rating_reporter', 'date']

    def create(self, validated_data):
        validated_data['rating_reporter'] = self.context['request'].user
        return super().create(validated_data)