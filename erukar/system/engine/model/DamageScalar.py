class DamageScalar:
    def __init__(self, raw, modifier, scale_amount=2.0, requirement=8.0, cutoff=200, percentage=1.0):
        self.raw = raw
        self.modifier = modifier
        self.scale_amount = scale_amount
        self.requirement = requirement
        self.cutoff = cutoff
        self.percentage = percentage

    def raw_unscaled(self):
        return self.raw * self.percentage

    def raw_scaled(self, lifeform):
        return self.raw_unscaled + self.scale_for(lifeform)

    def scale_for(self, lifeform):
        att = getattr(lifeform, self.modifier, 0)
        zero_corrected = max(0, att - self.requirement)
        capped = min(zero_corrected, self.cutoff)
        return (capped * self.scale_amount) + att
