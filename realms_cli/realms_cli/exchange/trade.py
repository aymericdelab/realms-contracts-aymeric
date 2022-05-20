# First, import click dependency
import click

from realms_cli.caller_invoker import wrapped_call, wrapped_send, compile, deploy
from realms_cli.config import Config, strhex_as_strfelt, safe_load_deployment
from realms_cli.shared import uint, expanded_uint_list, expanded_uint_list_decimals, uint_decimal
from realms_cli.deployer import logged_deploy
from realms_cli.utils import print_over_colums
import time


@click.command()
@click.option('--max_currency', type=click.STRING, help='Maximum to sell', prompt=True)
@click.option('--resource_ids', is_flag=False,
              metavar='<columns>', type=click.STRING, help='Resource Ids', prompt=True)
@click.option('--resource_values', is_flag=False,
              metavar='<columns>', type=click.STRING, help='Resource values', prompt=True)
@click.option("--network", default="goerli")
def buy_tokens(resource_ids, resource_values, max_currency, network):
    """
    Claim available resources
    """
    config = Config(nile_network=network)

    resource_ids = [c.strip() for c in resource_ids.split(',')]
    resource_values = [c.strip() for c in resource_values.split(',')]

    wrapped_send(
        network=config.nile_network,
        signer_alias=config.ADMIN_ALIAS,
        contract_alias="proxy_Exchange_ERC20_1155",
        function="buy_tokens",
        arguments=[
            *uint_decimal(max_currency),
            len(resource_ids),
            *expanded_uint_list(resource_ids),
            len(resource_ids),
            *expanded_uint_list_decimals(resource_values),
            int(time.time() + 3000)
        ],
    )


@click.command()
@click.option('--min_currency', type=click.STRING, help='Maximum to sell', prompt=True)
@click.option('--resource_ids', is_flag=False, metavar='<columns>', type=click.STRING, help='Resource Ids', prompt=True)
@click.option('--resource_values', is_flag=False,
              metavar='<columns>', type=click.STRING, help='Resource values', prompt=True)
@click.option("--network", default="goerli")
def sell_tokens(resource_ids, resource_values, min_currency, network):
    """
    Claim available resources
    """
    # split columns by ',' and remove whitespace
    resource_ids = [c.strip() for c in resource_ids.split(',')]
    resource_values = [c.strip() for c in resource_values.split(',')]

    config = Config(nile_network=network)

    wrapped_send(
        network=config.nile_network,
        signer_alias=config.ADMIN_ALIAS,
        contract_alias="proxy_Exchange_ERC20_1155",
        function="sell_tokens",
        arguments=[
            *uint_decimal(min_currency),
            len(resource_ids),
            *expanded_uint_list(resource_ids),
            len(resource_ids),
            *expanded_uint_list_decimals(resource_values),
            int(time.time() + 3000)
        ],
    )

@click.command()
@click.option("--network", default="goerli")
def get_all_sell_price(network):
    """
    Get all sell price
    """
    config = Config(nile_network=network)
    n_resources = len(config.RESOURCES)

    uints = []
    values = []
    for i in range(n_resources):
        uints.append(str(i+1))
        uints.append("0")
        values.append(1 * 10 ** 18)
        values.append("0")

    out = wrapped_call(
        network=config.nile_network,
        contract_alias="proxy_Exchange_ERC20_1155",
        function="get_all_sell_price",
        arguments=[
            n_resources,
            *uints,
            n_resources,
            *values,
        ],
    )
    
    out = out.split(" ")
    pretty_out = []
    for i, resource in enumerate(config.RESOURCES):
        pretty_out.append(f"1 {resource} sells {round(int(out[i*2+1], 16) / 1000000000000000000, 4)}  $LORDS")
    print('MARKET SELL PRICES PER LORDS')
    print_over_colums(pretty_out)


@click.command()
@click.option("--network", default="goerli")
def get_all_buy_price(network):
    """
    Get all buy price
    """
    # split columns by ',' and remove whitespace

    config = Config(nile_network=network)
    n_resources = len(config.RESOURCES)
    
    uints = []
    values = []
    for i in range(n_resources):
        uints.append(str(i+1))
        uints.append("0")
        values.append(1 * 10 ** 18)
        values.append("0")

    out = wrapped_call(
        network=config.nile_network,
        contract_alias="proxy_Exchange_ERC20_1155",
        function="get_all_buy_price",
        arguments=[
            n_resources,
            *uints,
            n_resources,
            *values,
        ],
    )
    
    out = out.split(" ")
    pretty_out = []
    for i, resource in enumerate(config.RESOURCES):
        pretty_out.append(f"1 {resource} buys {round(int(out[i*2+1], 16) / 1000000000000000000, 4)} $LORDS")
    print('MARKET BUY PRICES PER LORDS')
    print_over_colums(pretty_out)
