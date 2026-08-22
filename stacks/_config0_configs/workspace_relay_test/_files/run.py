"""Workspace relay validation stack for host-order workspace_id behavior."""


def _workspace_groups(stack):
    return stack.workspace_lay.name, stack.workspace_check.name


def _add_workspace_lay(stack, *, group, workspace_id):
    stack.add_groups_to_host(
        display=True,
        human_description="Lay a marker file into the shared workspace",
        workspace_id=workspace_id,
        automation_phase="validation",
        hostname=stack.hostname,
        groups=[group],
    )


def _add_workspace_check(stack, *, group, workspace_id):
    stack.add_groups_to_host(
        display=True,
        human_description="Assert the shared workspace contains the laid marker file",
        workspace_id=workspace_id,
        automation_phase="validation",
        hostname=stack.hostname,
        groups=[group],
    )


def _run_two_calls(stack, *, lay_group, check_group):
    workspace_id = stack.random_id(size=10)

    stack.set_parallel()
    _add_workspace_lay(stack, group=lay_group, workspace_id=workspace_id)
    stack.unset_parallel(wait_all=True)

    stack.set_parallel()
    _add_workspace_check(stack, group=check_group, workspace_id=workspace_id)
    stack.unset_parallel(wait_all=True)


def _run_isolation(stack, *, check_group):
    stack.set_parallel()
    _add_workspace_check(
        stack,
        group=check_group,
        workspace_id=stack.random_id(size=10),
    )
    stack.unset_parallel(wait_all=True)


def run(stackargs):
    stack = newStack(stackargs)

    stack.parse.add_required(key="hostname", types="str")
    stack.parse.add_required(
        key="mode",
        types="str",
        choices=["two_calls", "isolation"],
    )

    stack.add_execgroup("config0-hub:::ansible::workspace_lay", name="workspace_lay")
    stack.add_execgroup("config0-hub:::ansible::workspace_check", name="workspace_check")

    stack.init_variables()
    stack.init_execgroups()

    lay_group, check_group = _workspace_groups(stack)

    if stack.mode == "two_calls":
        _run_two_calls(stack, lay_group=lay_group, check_group=check_group)
    elif stack.mode == "isolation":
        _run_isolation(stack, check_group=check_group)
    else:
        raise ValueError(f"unsupported workspace relay mode: {stack.mode!r}")

    return stack.get_results()
