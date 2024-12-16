from flask import Flask, jsonify, request
import subprocess
import os
import docker
from functools import wraps

app = Flask(__name__)

# 从环境变量获取 API KEY
API_KEY = os.getenv('API_KEY', 'your-default-api-key')


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({'success': False, 'message': 'Invalid API key'}), 401

    return decorated


# Docker客户端
docker_client = docker.from_env()


@app.route('/sync', methods=['POST'])
@require_api_key
def sync_nginx_config():
    try:
        # 切换到配置目录
        os.chdir('/opt/nginx-config')

        # 执行git pull
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                'success': False,
                'message': f'Git pull failed: {result.stderr}'
            }), 500

        # 获取nginx容器
        nginx_container = docker_client.containers.get('nginx')

        # 执行nginx -s reload
        exec_result = nginx_container.exec_run('nginx -s reload')

        if exec_result.exit_code != 0:
            return jsonify({
                'success': False,
                'message': f'Nginx reload failed: {exec_result.output.decode()}'
            }), 500

        return jsonify({
            'success': True,
            'message': 'Nginx configuration synchronized and reloaded successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
