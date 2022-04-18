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

        # replacing dlt.read with the step function
        start = 'dlt.read('
        end = ')'

        while True:
            result = re.search('%s(.*)%s' % (start, end), side_step)

            if result:
                replace_with = side_step[result.start(
                    1)+1:result.end(1)-1].replace('"', '') + '()'
                side_step = side_step.replace(result.group(0), replace_with)

            else:
                break

        return side_step
