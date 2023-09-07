from monty.serialization import loadfn
from apex.core.common_equi import (make_equi, post_equi)
from apex.core.common_prop import (make_property, post_property)
from dflow.python import upload_packages
from apex.utils import get_task_type
upload_packages.append(__file__)


def run_step(parameter, step):
    # TODO: add local run step mode
    print('-------Singel step local debug mode--------')
    param_dict = loadfn(parameter[0])
    # check input args
    json_type = get_task_type(param_dict)
    mismatch1 = step in ['make_relax', 'post_relax'] and json_type == 'props'
    mismatch2 = step in ['make_post', 'post_props'] and json_type == 'relax'
    if mismatch1 or mismatch2:
        raise RuntimeError(
            f'mismatched indication step with type of json provided: {json_type}'
        )

    structures = param_dict["structures"]
    inter_parameter = param_dict["interaction"]
    if step in ['make_relax', 'post_relax']:
        param = param_dict["relaxation"]
        if step == 'make_relax':
            print('Making relaxation tasks locally...')
            make_equi(structures, inter_parameter, param)
        else:
            print('Posting relaxation results locally...')
            post_equi(structures, inter_parameter)
    else:
        param = param_dict["properties"]
        if step == 'make_props':
            print('Making properties tasks locally...')
            make_property(structures, inter_parameter, param)
        else:
            print('Posting properties results locally...')
            post_property(structures, inter_parameter, param)
