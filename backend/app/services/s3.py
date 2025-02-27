"""S3 Service module"""
import uuid
import boto3
from fastapi import UploadFile


class S3Service:
    """S3 Service class"""
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, 
                 region_name: str, endpoint_url: str, bucket_name: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Garantir que o bucket exista, criar se não existir"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
    
    async def upload_file(self, file: UploadFile) -> str:
        """Upload de arquivo para o S3 e retorno da URL"""
        # Gerar nome único para o arquivo
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        object_name = f"{uuid.uuid4()}.{file_extension}"
        
        # Ler o conteúdo do arquivo
        file_content = await file.read()
        
        # Upload para o S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=object_name,
            Body=file_content,
            ContentType=file.content_type
        )
        
        # Construir e retornar a URL do objeto
        if 'localstack' in self.s3_client.meta.endpoint_url:
            # Para LocalStack, a URL segue um formato específico
            return f"{self.s3_client.meta.endpoint_url}/{self.bucket_name}/{object_name}"
        else:
            # Para AWS real, o formato da URL é diferente
            return f"https://{self.bucket_name}.s3.{self.s3_client.meta.region_name}.amazonaws.com/{object_name}"
