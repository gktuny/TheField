from core.state import ExistenceState
class PromptEngine:
    def __init__(self, adapter, hooks):
        self.adapter = adapter
        self.hooks = hooks
    def run(self, ctx, prompt, signal):
        if ctx.state != ExistenceState.ACTIVE: return None
        self.hooks.before_response(ctx, signal)
        output = self.adapter.generate(prompt)
        self.hooks.after_response(ctx, output)
        return output