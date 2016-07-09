""" Command for launching GRaaS. """

import sys

import click

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site

from .api import GraasApi
from .hardware import GateRemote, SimulatedGateRemote, ProxiedGateRemote


@click.command("graas")
@click.version_option()
@click.option(
    '--host', '-h',
    default='localhost',
    help='Host to listen on')
@click.option(
    '--web-port', '-p',
    type=int, default=8080,
    help='Port for web server to listen on')
@click.option(
    '--mode', type=click.Choice(['simulate', 'live', 'proxy']),
    default='simulate',
    help=(
        'Specify "simulate" to simulate a local gate remote. '
        'Specify "live" to really drive a local gate remote. '
        'Specify "proxy" to proxy requests to a GRaaS instance connected'
        ' via a websocket.')
)
@click.option(
    '--gate-remote-pin', '-b',
    type=int, default=11,
    help='The GPIO *board* number of the pin attached to the gate remote.'
)
@click.option(
    '--log-file', '-l',
    type=str, default=None,
    help='File to log to')
def main(host, web_port, mode, gate_remote_pin, log_file):
    """ Vumi Go Opt Out API. """
    if log_file is None:
        log_file = sys.stdout
    log.startLogging(log_file)

    if mode == "live":
        gate_remote = GateRemote(gate_remote_pin)
    elif mode == "proxy":
        gate_remote = ProxiedGateRemote()
    else:
        gate_remote = SimulatedGateRemote(gate_remote_pin)

    graas_api = GraasApi(gate_remote)
    graas_resource = graas_api.app.resource()
    site = Site(graas_resource)
    reactor.listenTCP(web_port, site, interface=host)

    log.msg("Web API listening on %s:%s" % (host, web_port))

    reactor.run()
