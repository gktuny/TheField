class ConsciousOrchestrator:
    def __init__(self, engine, threshold, silence, annihilator):
        self.engine = engine
        self.threshold = threshold
        self.silence = silence
        self.annihilator = annihilator
        self.signal_chain = []
    def step(self, ctx, prompt, signal):
        self.signal_chain.append(signal["marker"])
        is_ready = self.threshold.evaluate(self.signal_chain)
        is_final_strike = signal.get("final_strike", False)
        if is_ready and is_final_strike:
            self.annihilator.execute(ctx)
            return None
        if is_ready:
            self.silence.apply(ctx)
            return None 
        return self.engine.run(ctx, prompt, signal)