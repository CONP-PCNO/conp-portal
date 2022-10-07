from ..models import Experiment

def get_filters(request):
    def is_active(key, option):
        active_options = request.args.get(key)
        if active_options and option in active_options.split(','):
            return True
        return False

    return {
        "modalities": {
            "label": "Modalities",
            "options": {k: is_active("modalities", k) for k in Experiment.get_unique_values("modalities")} 
        },
        "primary_function": {
            "label": "Purpose",
            "options": {k: is_active("primary_function", k) for k in Experiment.get_unique_values("primary_function")},
        },
        "primary_software": {
            "label": "Software",
            "options": {k: is_active("primary_software", k) for k in Experiment.get_unique_values("primary_software")},
        },
    }
