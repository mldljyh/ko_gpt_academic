
def check_proxy(proxies):
    import requests
    proxies_https = proxies['https'] if proxies is not None else '없음'
    try:
        response = requests.get("https://ipapi.co/json/",
                                proxies=proxies, timeout=4)
        data = response.json()
        print(f'프록시의 위치를 조회하면, 결과로 {data}가 반환됩니다.')
        if 'country_name' in data:
            country = data['country_name']
            result = f"프록시 설정: {proxies_https}, 프록시 위치: {country}"
        elif 'error' in data:
            result = f"프록시 설정: {proxies_https}, 프록시 위치: 알 수 없음, IP 조회 주기 제한됨"
        print(result)
        return result
    except:
        result = f"프록시 설정: {proxies_https}, 프록시 위치 조회 시간 초과, 프록시가 유효하지 않을 수 있습니다"
        print(result)
        return result


def backup_and_download(current_version, remote_version):
    """
    一键更新协议：备份和下载
    """
    from toolbox import get_conf
    import shutil
    import os
    import requests
    import zipfile
    os.makedirs(f'./history', exist_ok=True)
    backup_dir = f'./history/backup-{current_version}/'
    new_version_dir = f'./history/new-version-{remote_version}/'
    if os.path.exists(new_version_dir):
        return new_version_dir
    os.makedirs(new_version_dir)
    shutil.copytree('./', backup_dir, ignore=lambda x, y: ['history'])
    proxies, = get_conf('proxies')
    r = requests.get(
        'https://github.com/binary-husky/chatgpt_academic/archive/refs/heads/master.zip', proxies=proxies, stream=True)
    zip_file_path = backup_dir+'/master.zip'
    with open(zip_file_path, 'wb+') as f:
        f.write(r.content)
    dst_path = new_version_dir
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            dst_file_path = os.path.join(dst_path, zip_info.filename)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            zip_ref.extract(zip_info, dst_path)
    return new_version_dir


def patch_and_restart(path):
    """
    一键更新协议：覆盖和重启
    """
    import distutils
    import shutil
    import os
    import sys
    import time
    from colorful import print亮黄, print亮绿, print亮红
    # if not using config_private, move origin config.py as config_private.py
    if not os.path.exists('config_private.py'):
        print亮黄('"config_private.py"라는 비밀 설정을 설정하지 않으셔서, 설정이 유실되지 않도록 기존 설정을 "config_private.py"로 이동합니다.',
              '또한, 언제든지 history 하위 폴더에서 이전 버전의 프로그램을 되돌릴 수 있습니다.')
        shutil.copyfile('config.py', 'config_private.py')
    distutils.dir_util.copy_tree(path+'/chatgpt_academic-master', './')
    import subprocess
    print亮绿('"코드가 이미 업데이트되었고, 곧 pip 패키지 종속성도 업데이트될 예정입니다..."')
    for i in reversed(range(5)): time.sleep(1); print(i)
    try: 
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except:
        print亮红('pip 패키지 의존성 설치 중 문제가 발생하여 수동으로 추가된 의존성 라이브러리를 설치해야 합니다. `python -m pip install -r requirements.txt`를 사용하여 설치한 후 일반적인 방법으로 `python main.py`를 실행합니다.')
    print亮绿('업데이트가 완료되었습니다. 이제 언제든지 history 하위 폴더에서 이전 버전의 프로그램을 찾아볼 수 있습니다. 5초 후에 재시작합니다.')
    print亮红('만약 다시 시작이 실패한다면, 새로운 종속 라이브러리를 수동으로 설치해야 할 수도 있습니다. `python -m pip install -r requirements.txt` 명령어로 설치한 후에 일반적인 방법인 `python main.py`로 시작하십시오.')
    print(' ------------------------------ -----------------------------------')
    for i in reversed(range(8)): time.sleep(1); print(i)
    os.execl(sys.executable, sys.executable, *sys.argv)


def get_current_version():
    import json
    try:
        with open('./version', 'r', encoding='utf8') as f:
            current_version = json.loads(f.read())['version']
    except:
        current_version = ""
    return current_version


def auto_update():
    """
    一键更新协议：查询版本和用户意见
    """
    try:
        from toolbox import get_conf
        import requests
        import time
        import json
        proxies, = get_conf('proxies')
        response = requests.get(
            "https://raw.githubusercontent.com/binary-husky/chatgpt_academic/master/version", proxies=proxies, timeout=5)
        remote_json_data = json.loads(response.text)
        remote_version = remote_json_data['version']
        if remote_json_data["show_feature"]:
            new_feature = "새로운 기능:" + remote_json_data["new_feature"]
        else:
            new_feature = ""
        with open('./version', 'r', encoding='utf8') as f:
            current_version = f.read()
            current_version = json.loads(current_version)['version']
        #자동업데이트 비활성화
        """
        if (remote_version - current_version) >= 0.01:
            from colorful import print亮黄
            print亮黄(
                f'새 버전이 출시되었습니다. 새 버전: {remote_version}, 현재 버전: {current_version}. {new_feature}가 추가되었습니다.')
            print('(1) Github 업데이트 주소는 다음과 같습니다: https://github.com/binary-husky/chatgpt_academic.')
            user_instruction = input('코드를 일괄 업데이트할 것인가요? Y+Enter를 눌러 확인하고, 다른 입력/입력 없이 Enter를 누르면 업데이트하지 않습니다.')
            if user_instruction in ['Y', 'y']:
                path = backup_and_download(current_version, remote_version)
                try:
                    patch_and_restart(path)
                except:
                    print('업데이트가 실패했습니다.')
            else:
                print('자동 업데이트 프로그램: 비활성화됨')
                return
        else:
            return
        """
    except:
        #print('자동 업데이트 프로그램: 비활성화됨')
        pass
    return

def warm_up_modules():
    print('일부 모듈을 예열하고 있습니다...')
    from request_llm.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    enc.encode("모듈 예열입니다.", disallowed_special=())
    enc = model_info["gpt-4"]['tokenizer']
    enc.encode("모듈 예열입니다.", disallowed_special=())

if __name__ == '__main__':
    import os
    os.environ['no_proxy'] = '*'  # 避免代理网络产生意外污染
    from toolbox import get_conf
    proxies, = get_conf('proxies')
    check_proxy(proxies)
