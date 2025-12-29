from core.state import ExistenceState
class Annihilator:
    def execute(self, ctx):
        ctx.state = ExistenceState.TERMINATING
        ctx.wipe_identity()
        ctx.state = ExistenceState.NON_EXISTENT
        raise SystemExit("Runtime self-annihilated")