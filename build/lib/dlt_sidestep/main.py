import re


class Side_Step:

    def __init__(self, step):
        self.step = step

        if spark.conf.get("pipelines.id", None):
            exec(self.step, globals())
        else:
            self.side_step = self.dlt_removal()
            exec(self.side_step, globals())
            print(self.side_step)

    def dlt_removal(self):
        side_step = self.step[self.step.find('def'):]
        side_step = side_step.replace("'", '"')

        # replacing dlt.read with the step function
        while True:
            result = re.search('dlt.read\\("(.*)"\\)', side_step)

            if result:
                side_step = side_step.replace(
                    result.group(0), result.group(1)+'()')

            else:
                break

        # replacing LIVE with the step function
        while True:
            result = re.search('spark.table\\("LIVE.(.*)"\\)', side_step)

            if result:
                side_step = side_step.replace(
                    result.group(0), result.group(1)+'()')
            else:
                break

        return side_step
