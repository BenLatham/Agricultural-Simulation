from simulation.models.diet_models import Feed, FeedType
import csvReader.csvReader2 as csv
import simulation.models.utilities as model_util
from django.conf import settings
FEEDS_DIR = settings.FEEDS_DIR

class FeedLoader:
    def __init__(self, scenario):
        self.scenario = self.scenario

    def load_feeds(self):
        type_data = self._read_types_file()
        feed_data = self._read_feeds_file()
        types_records = [FeedType(scenario=self.scenario, name=record[0], minInclusion=record[1], maxInclusion=record[2]) for record in type_data]
        types_dict = model_util.save_get(types_records, FeedType, self.scenario)
        feed_records = [Feed(scenario=self.scenario, name=record[0], me=record[0], fme=record[1], erdp=record[2], dup=record[3], adf=record[4], feed_type=types_dict[record[5]], price=record[6]) for record in feed_data]
        model_util.save_all(feed_records, Feed)



    def _read_types_file(self):
        fields = csv.fields([
            ["name"],
            ["minInclusion","float"],
            ["maxInclusion","float"]
        ])
        return csv.read(FEEDS_DIR, "types.csv", fields)

    def _read_feeds_file(self):
        fields = csv.fields([
            ["name"],
            ["me", "float"],
            ["fme", "float"],
            ["erdp", "float"],
            ["dup", "float"],
            ["adf", "float"],
            ["feed_type"],
            ["maxInclusion", "float"],
            ["price", "float"]
        ])
        return csv.read(FEEDS_DIR, "feeds.csv", fields)

class Diet:
    def __init__(self, scenario, feeds=None):
        self.types = self._get_types_dict(scenario)
        self._load_diet(feeds, scenario)
        self.percents = [0]*len(self.diet)

    def __len__(self):
        return len(self.diet)

    def __getattr__(self, name):
        if name in Feed.aggregable:
            return self._total(name)
        raise AttributeError()

    def proportion(self, index):
        return self.percents[index]/100

    def set_proportion(self, index, value):
        self.percents[index]=int(value*100)

    def is_formulated(self):
        """
        :return: True if the feeds add up to 100%, else false
        """
        if sum(self.percents)==100:
            return True
        return False

    def mp(self, target_yield):
        """
        Calculate the metabolisable protein in a given diet

        :param FME: Fermentable Metabolisable Energy
        :param ERDP: Effective Rumen Degradable Protein
        :param DUP: Digestible Undegradable Protein
        :param targetYield: Target Microbial Protein Yield
        :return: float, metabolisable protein

        """
        dmtp = self.dmtp(target_yield)
        return dmtp + self.dup


    def mcp(self, target_yield):
        """
        Calculate the microbial Crude protein yield of the diet
        :param targetYield: Target Microbial Protein Yield
        :return: float, microbial crude protein

        """
        if (self.erdp / self.fme > target_yield):
            return self.fme*target_yield
        else:
            return self.erdp

    def dmtp(self, target_yield):
        """
        calculate digestible microbial true protein given the amount of microbial crude protein

        :param MCP: Microbial Crude Protein
        :return: float, digestible microbial true protein
        """
        mcp = self.mcp(target_yield)
        mtp = mcp * 0.75  # estimated fraction true protein
        dmtp = mtp * 0.85  # estimated fraction digestible
        return dmtp

    def _total(self, component):
        total = 0
        for index, feed in enumerate(self.diet):
            total += feed[component] * self.percents[index]
        return total

    def _load_diet(self, feeds, scenario):
        self.diet =[]
        if feeds is not None:
            self.diet+=feeds
        self._add_stored_feeds(scenario)

    def _add_stored_feeds(self, scenario):
        for feed in Feed.objects.filter(scenario=scenario):
            self.diet.append(feed.to_dict)

    def _get_types_dict(scenario):
        return {
            feed_type.id: feed_type.to_dict() for feed_type in
            FeedType.objects.filter(scenario=scenario)
            }


def balance(diet, cow):
    current = diet.percents.copy()


def permutations(n, total, depth=0):
    max_inc_result = max_inc(depth)
    min_inc_result = min_inc(depth)

    if n == 1:
        if max_inc_result >= total >= min_inc_result:
            yield (total,)
    else:
            for i in range(min(max_inc_result, total), min_inc_result-1, -1):
                for j in permutations(n - 1, total - i, depth+1):
                    yield (i,) + j


def max_inc(feed):
    return 100


def min_inc(feed):
    return 0
