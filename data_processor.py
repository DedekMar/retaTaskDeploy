import lxml.etree as ET



class DataProcessor:

    def __init__(self, file_path):
        """
        Initializes a new DataProcessor object with the specified XML file_path

        Parameters:
            file_path (str): The path to the XML file to be processed.

        Returns:
            None
        """
        self.root = self.open_xml_file(file_path)

    def open_xml_file(self, file_path):
        """
        Opens and parses the XML file, returns its root.

        Parameters:
            file_path (str): The path to the XML file.

        Returns:
            xml.etree.ElementTree.Element: The root element of the XML tree, or None if there was an error.
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            return root
        
        except Exception as e:
            print(f"Error occurred during parsing of the XML: {e}")
            return None

    def get_all_items(self):
        """
        Retrieves all items from the XML file node items.

        Returns:
            List[xml.etree.ElementTree.Element]: A list of all item elements found in the XML file.
        """        
        items_element = self.root.find('items')

        # Count the number of child 'item' elements in 'items'
        if items_element is not None:
            all_items = items_element.findall('./item')
            return all_items
        else:
            return []

    def count_all_items(self):
        """
        Counts the total number of items in the XML file node items.

        Returns:
            int: The number of items found in the XML file.
        """
        all_items_count = len(self.get_all_items())
        return all_items_count

    def get_all_item_names(self):
        """
        Retrieves the names of all items from the XML file node items.

        Returns:
            List[str]: A list of names of all items found in the XML file.
        """
        all_items = self.get_all_items()
        item_names = [item.get('name') for item in all_items if item is not None]

        return item_names

    def get_items_with_category_parts(self, category_id):
        """
        Retrieves items along with their spare parts based on the specified category ID.

        Parameters:
            category_id (str): The ID of the category for filtering spare parts.

        Returns:
            List[dict]: A list of dictionaries, each containing information about an item and its spare parts.
        """        
        # Find all items that have spares using xpath 
        items_with_parts = self.root.xpath(f"./items/item[descendant::parts/part[@categoryId='{category_id}']/item]")
        items_with_parts_list = []

        for item in items_with_parts:
            item_code = item.get("code")
            item_name = item.get("name")

            # Find all part elements with the specified category_id with xpath
            parts = item.findall(f'./parts/part[@categoryId="{category_id}"]/item')
            item_parts = [
                {
                    'code': part.get('code'),
                    'name': part.get('name')
                }
                for part in parts
            ]
            items_with_parts_list.append({
                "code": item_code,
                "name": item_name,
                "category_parts": item_parts
            })

        return items_with_parts_list