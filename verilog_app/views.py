import json
from django.shortcuts import render

# Create your views here.
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
# Define the Swagger schema for the request body
verilog_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='The Verilog code to compile'
        )
    },
    required=['code']
)


@csrf_exempt
@swagger_auto_schema(
    method='post',
    request_body=verilog_request_body,
    responses={
        200: openapi.Response(
            description="Compilation result",
            examples={
                'application/json': {
                    'success': True,
                    'output': 'Hello, Verilog\n',
                    'errors': ''
                }
            }
        ),
        400: openapi.Response(
            description="Invalid request",
            examples={
                'application/json': {
                    'success': False,
                    'errors': 'Invalid JSON body or missing required fields'
                }
            }
        ),
    }
)
@api_view(['POST'])
def compile_verilog(request):
    # print(request.body)
    if request.method == 'POST':
        body = json.loads(request.body)
        verilog_code = body.get('code', '')
        # Save code to a temporary file
        file_path = '/tmp/top.v'
        with open(file_path, 'w') as f:
            f.write(verilog_code)

        try:
            # Run iverilog to compile the code
            compile_process = subprocess.run(
                ['iverilog', '-o', 'top.out', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Run the output file if no errors
            if compile_process.returncode == 0:
                run_process = subprocess.run(
                    ['vvp', 'top.out'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                return JsonResponse({
                    'success': True,
                    'output': run_process.stdout,
                    'errors': run_process.stderr
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': compile_process.stderr
                })
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})
