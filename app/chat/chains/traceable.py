class TraceableChain:
    def __call__(self, *args, **kwargs):
        print(self.metadata)
        return super().__call__(*args, **kwargs)