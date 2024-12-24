from hurry.filesize import size

from flask_restful import Resource
from pylon.core.tools import web, log  # pylint: disable=E0611,E0401
from tools import MinioClient, auth


class API(Resource):
    url_params = [
        '<int:result_id>',
    ]

    def __init__(self, module):
        self.module = module

    @auth.decorators.check_api(["configuration.artifacts.artifacts.view"])
    def get(self, result_id: int):
        test_data = self.module.context.rpc_manager.call.backend_results_or_404(run_id=result_id)
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id=test_data.project_id)
        s3_settings = test_data.test_config.get(
            'integrations', {}).get('system', {}).get('s3_integration', {})
        minio_client = MinioClient(project, **s3_settings)
        bucket_name = str(test_data.name).replace("_", "").replace(" ", "").lower()
        minio_files = minio_client.list_files(bucket_name)
        files = []
        build_id: str = test_data.build_id
        custom_files_prefix = f'reports_test_results_{build_id}'
        log_file_name = f'{build_id}.log'
        ai_summary_file_name = f'{build_id}_llm_reports.zip'
        for f in minio_files:
            name: str = f["name"]
            if name == log_file_name or name.startswith(custom_files_prefix) or name == ai_summary_file_name:
                f["size"] = size(f["size"])
                files.append(f)
        return files, 200
