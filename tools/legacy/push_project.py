"""Direct project Git push helper. Never displays or passes credentials in argv."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import time
from urllib.parse import urlsplit


def load_connection(path, endpoint):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd) as stream:
        info=os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid() or info.st_mode&0o077 or info.st_size>16384:
            raise ValueError('private_connection_required')
        value=json.load(stream)
    parsed=urlsplit(endpoint)
    if (set(value)!={'project_id','git_url','username','access_token','expires_at'} or
        parsed.scheme!='https' or not parsed.hostname or parsed.port not in (None,443) or not any(parsed.hostname.endswith('.'+domain) for domain in ('reefy.dev','reefy.ai')) or parsed.username or parsed.password or
        not re.fullmatch(r'/git/[a-f0-9]{32}\.git', parsed.path) or parsed.query or parsed.fragment or value['git_url']!=endpoint or
        not re.fullmatch('[a-f0-9]{32}', str(value['project_id'])) or parsed.path!='/git/'+value['project_id']+'.git' or value['username']!='git' or
        not re.fullmatch('[A-Za-z0-9_.-]{32,4096}',str(value['access_token'])) or
        type(value['expires_at']) not in (int,float) or not time.time()<value['expires_at']<=time.time()+900):
        raise ValueError('invalid_project_connection')
    return value


def push(connection,endpoint,repo):
    value=load_connection(connection,endpoint);repo=Path(repo).resolve()
    if not repo.is_dir() or not (repo/'.git').is_dir(): raise ValueError('local_git_project_required')
    commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','--verify','HEAD'],text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}',commit): raise ValueError('exact_commit_required')
    auth=base64.b64encode(('git:'+value['access_token']).encode()).decode()
    env={key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
    settings=[('http.'+endpoint+'.extraHeader','Authorization: Basic '+auth),
        ('http.followRedirects','false'),('http.sslVerify','true'),('credential.helper',''),('core.hooksPath','/dev/null')]
    env.update({'GIT_TERMINAL_PROMPT':'0','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull,
                'GIT_CONFIG_COUNT':str(len(settings))})
    for index,(key,val) in enumerate(settings):
        env['GIT_CONFIG_KEY_'+str(index)]=key;env['GIT_CONFIG_VALUE_'+str(index)]=val
    proc=subprocess.run(['git','-C',str(repo),'push','--porcelain',endpoint,'HEAD:refs/heads/main'],
        env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)
    if proc.returncode: raise ValueError('direct_git_push_failed')
    return {'commit':commit,'pushed':True,'helper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--connection',type=Path,required=True)
    p.add_argument('--endpoint',required=True);p.add_argument('--repo',type=Path,required=True);args=p.parse_args()
    try: print(json.dumps(push(args.connection,args.endpoint,args.repo)))
    except (ValueError,OSError,subprocess.SubprocessError): raise SystemExit('Project Git push failed; credentials omitted')
