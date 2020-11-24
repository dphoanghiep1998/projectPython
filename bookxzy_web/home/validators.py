import os
from django.core.exceptions import ValidationError
#Trình xác nhận nội dung tệp tải lên

def validate_ContentChapter(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File không hợp lệ , chỉ chấp nhận file ,txt')
