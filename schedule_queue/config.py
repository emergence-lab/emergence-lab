def get_tool_info(slug):
    return tool[slug]


# custom attributes for tools
tool = {
    'd180-growth': {
        'max_reservations': 8,
        'process_start_url': 'create_growth_d180_start',
    },
    'd75-growth': {
        'max_reservations': 8,
    },
}
