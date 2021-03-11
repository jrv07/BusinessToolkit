from module_processing.animator.instructions import instructions as animator_instructions
from module_processing.arrk.instructions import instructions as arrk_instructions
from module_processing.metapost.instructions import instructions as metapost_instructions

instructions = [
    *animator_instructions,
    *arrk_instructions,
    *metapost_instructions
]
