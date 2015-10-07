__author__ = 'yingbozhan'


parse_segment = """
def parse_segment(query, single_segment_information):
    time_format = {time_format}
    return c.segment_factory(
        query,
        mode='flight',
        from_place=c.geo_place_factory(code=single_segment_information.xpath({xpath_from_code}), namespace='iata', type='airport'),
        to_place=c.geo_place_factory(code=single_segment_information.xpath({xpath_to_code}), namespace='iata', type='airport'),
        dep_time=c.DateTime({inline_dep_time}, strf=time_format),
        arr_time=c.DateTime({inline_arr_time}, strf=time_format),
        marketing_carrier_id=dict('iata': {inline_carrier}),
        marketing_segment_code={inline_flight_number},
        operating_carrier_id=dict('iata': {inline_carrier}),
        operating_segment_code={inline_flight_number},
        cabin_class=query.cabin_class ,
    )
"""



parse_segments = """
def parse_segments(query, segments_information):
    segments_dict = dict(
        price=None,
        segments=[]
    )
    segments = []
    for segment_information in segments_information.xpath_all({xpath_segment}):
        segment = parse_segment(query, segment_information)
        segments.append(segment)

    {function_caller_get_bound_price}
    segments = sort_segment(segments)
    segments_dict['segments'] = segments
    return segments_dict
"""


parse_quotes_without_mapping = """
def parse_quotes(query, quotes_information):
    quotes = []
    for quote_information in quotes.information.xpath_all({xpath_quote}):
        quote = parse_quote(query, quote_information)
        quotes.append(quote)
    return quotes
"""

parse_quote_without_mapping = """
def parse_quote(query, quote_information):
    segment_details = parse_segments(query, {xpath_segments})
    {function_to_combine_price}
    quote = c.transport_quote_factory(
        query,
        currency={inline_to_get_currency},
        total={inline_to_get_price},
        query_legs=range(len(query.legs)),
        can_be_one_way=True if query.one_way else False,
        can_be_outbound=False,
        can_be_inbound=False,
        {enable_deeplink_data}deeplink_data=c.Deeplink(c.Request(deeplink), c.BookingPage())
    )
    return quote
"""



register = """
register = c.register_transport(
    scrape,
    support=c.PricingSupport(
        reviewed_date=c.DateTime(2015, 1, 6),
        possible='L',
        implemented='L',
        source='API/Scrape',
        notes='',
        passenger_limits='',
        speedweaver_version='4'
    ),
    supported_types=['S'],
    modes=['flights'],
    query_validation=is_valid,
    deeplink_cache_settings=c.DeeplinkCacheSettings(600, 0)
)
"""