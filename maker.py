import shutil
from sh import python3
from config_reader import read_config

def make_component(name, destination):
    try:
        shutil.rmtree(destination)
    except OSError:
        #It's fine if it doesn't exist already
        pass
    source = '.components/%s' % name
    shutil.copytree(source, destination)
    try:
        shutil.rmtree(destination + '/.git')
    except OSError:
        #It's fine if it doesn't exist already
        pass

def make_template(name, destination):
    try:
        shutil.rmtree(destination)
    except OSError:
        #It's fine if it doesn't exist already
        pass
    source = '.components/%s/templates' % name
    run_codegen(source, destination)

def run_codegen(templates, destination):
    python3('.components/codegen/gen.py', template=templates,
            output=destination)

def make_all(location = 'components.yaml'):
    data = read_config(location)
    components = data.get('components', {})
    templates = data.get('templates', {})

    for key, value in components.items():
        print 'building %s' % key
        make_component(key, value['destination'])
    for key, value in templates.items():
        print 'building %s' % key
        make_template(key, value['destination'])
