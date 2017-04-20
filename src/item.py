class Item:
    """Defines an item object. The item typically will have a name, value,
    weight and possibly a list of tags or related info."""

    itemName = ""
    itemValue = ""
    itemWeight = 0
    itemInfo = []

    def __init__(self, itemName, itemValue, itemWeight, itemInfo):
        """Constructor for the class.

        :param itemName: Name of the item.
        :param itemValue: String that contains the numeric value of an item
        followed by its denomination. Ex: 5g is 5 gold, or 20s is 20 silver.
        :param itemWeight: Float that contains the item value in lb.
        :param itemInfo: List of associated tags of the item, usually empty.
        """
        self.itemName = itemName
        self.itemInfo = itemInfo
        self.itemValue = itemValue
        self.itemWeight = itemWeight

    def __repr__(self):
        """
        Streing representation of the object.
        :return: String s that contains all the object data.
        """
        s = ""
        s += "This is (a) %s worth %s. The %s weighs %0.1f lb." % \
             (self.itemName, self.itemValue, self.itemName, self.itemWeight)

        if (self.itemInfo != []):
            s += "Also, the item has the following special properties: " + \
                 str(self.itemInfo)

        return s

    @staticmethod
    def loadItemManifest(fname):
        """
        Loads the items and information from the manifest into a dict.
        :param fname: File containing information about different objects.
        :return: Dictionary with key-value store of itemName and item.
        """
        manifest = {}
        file = open(fname)

        for line in file:
            line = line.strip()
            itemName = ""
            itemValue = ""
            itemWeight = 0
            itemInfo = []

            # skip the line if it is empty or starts with #
            if not line.startswith("#"):
                args = line.split(" ")
                # check that atleast 3 arguments are passed in, else skip the
                # line
                if len(args) > 2:
                    # parse iteminfo for spaces
                    # DEBUG: possible bug if "_" character isnt removed.
                    itemName = args[0]
                    itemName = " ".join(itemName.split("_"))

                    # parse itemValue to see if the denomination is specified
                    itemValue = args[1]
                    if itemValue[-1] not in ['g', 's', 'c']:
                        itemValue += 'g'

                    # parse itemWeight
                    itemWeight = float(args[2])

                    # if there is any item info associated, add it.
                    if len(args) > 3:
                        itemInfo = args[3:]
                        for elem in itemInfo:
                            elem = " ".join(elem.split("_"))

                    # finally, make a new item object and store it in the
                    # item manifest with its name as key and item object as
                    # value

                    item = Item(itemName, itemValue, itemWeight, itemInfo)
                    manifest[itemName] = item

        # Close file when its no longer needed
        file.close()
        return manifest
