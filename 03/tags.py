import collections
import difflib
import xml.etree.ElementTree as ET

TOP_NUMBER = 10
RSS_FEED = 'rss.xml'
SIMILAR = 0.87

def get_tags():
    """Find all tags in RSS_FEED.
    Replace dash with whitespace."""
    result = []
    tree = ET.parse(RSS_FEED)
    root = tree.getroot()
    channel = root[0]
    for child in channel:
        if child.tag != "item":
            continue
        for subelem in child:
            if subelem.tag != "category":
                continue
            result.append(subelem.text.lower().replace('-', ' '))
    return result


def get_top_tags(tags):
    """Get the TOP_NUMBER of most common tags"""
    return collections.Counter(tags).most_common(TOP_NUMBER)


def get_similarities(tags):
    """Find set of tags pairs with similarity ratio of > SIMILAR"""
    result = set()
    result_list = list(set(tags))
    for idx, item in enumerate(result_list):
        for other in result_list[idx + 1:]:
            seqm = difflib.SequenceMatcher(None, item, other)
            if seqm.ratio() > SIMILAR:
                result.add(tuple(sorted([item, other])))
    return result


if __name__ == "__main__":
    tags = get_tags()
    top_tags = get_top_tags(tags)
    print('* Top {} tags:'.format(TOP_NUMBER))
    for tag, count in top_tags:
        print('{:<20} {}'.format(tag, count))
    similar_tags = dict(get_similarities(tags))
    print()
    print('* Similar tags:')
    for singular, plural in similar_tags.items():
        print('{:<20} {}'.format(singular, plural))
