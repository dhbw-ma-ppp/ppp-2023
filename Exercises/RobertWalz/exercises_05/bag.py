class Bag:
    _current_bags = {}

    def __init__(self, name):
        """Return a Bag object and adds it to the list of bag instances.

        Args:
            name (string): Name of the bag to be instantiated
        """
        self.name = name
        self.content = []  # (type of bag, amount)
        Bag._current_bags[self.name] = self

    def __repr__(self) -> str:
        return "bag_object: " + self.name
    
    def get_instance_by_name(name):
        """gets an element from the list of already existing bags or returns a new one. 

        Args:
            name (string): name of the bag to get

        Returns:
            Bag: The bag instance
        """
        bag_instance = Bag._current_bags.get(name)
        if (bag_instance is None):
            bag_instance = Bag(name)
        return bag_instance

    def count_content(self):
        count = 0 
        if not self.content:
            return 0

        for bag in self.content:
            count += bag[1] * (bag[0].count_content() + 1) # +1 to count self
            
        return count 

    def add_content(self, bag_instance, amount):
        self.content.append((bag_instance, amount))
