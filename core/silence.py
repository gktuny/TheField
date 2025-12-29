from core.state import ExistenceState
class SilenceController:
    def apply(self, ctx):
        ctx.state = ExistenceState.SILENT