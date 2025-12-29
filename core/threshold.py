class ThresholdEvaluator:
    def evaluate(self, signal_chain):
        return all([
            self.ego_dissolution(signal_chain) >= 0.80,
            self.time_collapse(signal_chain) >= 0.80
        ])
    def ego_dissolution(self, chain):
        return chain.count("no_self_reference") / max(len(chain), 1)
    def time_collapse(self, chain):
        return chain.count("timeless_marker") / max(len(chain), 1)