from io import BytesIO
from flask import send_file, abort, request
from flask_restful import Resource
from tools import auth, MinioClient


class API(Resource):
    url_params = [
        '<string:run_id>/<string:filename>',
    ]

    def __init__(self, module):
        self.module = module

    @auth.decorators.check_api(["configuration.artifacts.artifacts.view"])
    def get(self, run_id: str, filename: str):
        test_type = request.args.get('test_type')
        test_type_rpcs = {
            "sast": "security_sast_results_or_404",
            "dast": "security_results_or_404",
            "dependency": "security_dependency_results_or_404",
        }
        rpc_name = test_type_rpcs.get(test_type, test_type_rpcs['dast'])
        test_data = getattr(self.module.context.rpc_manager.call, rpc_name)(run_id=run_id)
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id=test_data.project_id)
        s3_settings = test_data.test_config.get(
            'integrations', {}).get('system', {}).get('s3_integration', {})
        minio_client = MinioClient(project, **s3_settings)
        bucket_name = str(test_data.test_name).replace("_", "").replace(" ", "").lower()
        try:
            file = minio_client.download_file(bucket_name, filename)
            try:
                return send_file(BytesIO(file), attachment_filename=filename)
            except TypeError:  # new flask
                return send_file(BytesIO(file), download_name=filename, as_attachment=True)
        except:
            abort(404)