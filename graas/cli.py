""" Command for launching GRaaS. """

import sys

import click

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site

from .api import GraasApi
from .hardware import GateRemote


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
    '--simulate/--live', default=True,
    help='Specify --live to really drive the gate.'
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
def main(host, web_port, simulate, gate_remote_pin, log_file):
    """ Vumi Go Opt Out API. """
    if log_file is None:
        log_file = sys.stdout
    log.startLogging(log_file)

    gate_remote = GateRemote(gate_remote_pin, simulate=simulate)
    graas_api = GraasApi(gate_remote)

    site = Site(graas_api.app.resource())
    reactor.listenTCP(web_port, site, interface=host)

    log.msg("Web API listening on %s:%s" % (host, web_port))

    reactor.run()
