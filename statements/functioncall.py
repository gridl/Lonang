from .statement import Statement
from .utils import helperassign
from functions import Function


def functioncall(c, m):
    """Function call. For instance:
        dx = someMethod(8)
    """
    assigned_to = m.group(1)
    name = m.group(2)
    params = Function.get_params(m.group(3))

    # Find the function
    function = c.find_matching_function(
        name=name,
        param_count=len(params),
        must_return=assigned_to is not None
    )

    if function is None:
        raise ValueError(
            f'No function called {name} with {len(params)} argument(s) exists')

    # We have a function, now copy the parameters if required
    for caller_p, func_p in zip(params, function.params):
        if caller_p != func_p:
            # Caller parameter and function parameter differs, we need to move
            c.add_code(helperassign(func_p, caller_p))

    # Parameters are ready, call the function
    c.add_code(f'call {name}')

    # Copy the result back if it differs from where the function stored it
    if assigned_to is not None and function.returns != assigned_to:
        c.add_code(helperassign(assigned_to, function.returns))


functioncall_statement = Statement(
    r'(?:(\w+) = )?(\w+)\(([\w, ]+)\)',
    functioncall
)
