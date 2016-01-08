Voice & other interfaces for GRaaS
==================================

The Cape Town office parking lot gate is open and closed by radio remote.
We have one remote per parking bay but often the set of people with remotes is
not the set of people who need to park. Many local employees are not at the
office regular and there are often visitors and guests who need to park.

We have built a small circuit board to connect a gate remote to a Raspberry Pi
and installed the circuit board and Pi in a box in the office.

The next step is to create user interfaces to the Pi and remote that allow
people to open and close the gate.

For a first user interface we thought it might be fun to try install
`Jasper <https://jasperproject.github.io/>`_ and write an extension for it that
toggles the remote.

We can also look at creating other interfaces, e.g.

* USSD interface (a Vumi Go Javascript sandbox application)
* A mobi site (using localStorage or serviceWorkers to make loading it fast)

People to poke: Simon Cross (hodgestar), Rudi Giesler (rudigiesler)


Useful links
------------

For the Raspberry Pi A+:

* `GPIO Zero <http://pythonhosted.org/gpiozero/>`_
* `Pi A+ GPIO <http://pi4j.com/images/j8header-a-plus.png>`_

For the voice interface:

* `Jasper <https://jasperproject.github.io/>`_

For the USSD interface:

* `Jsbox Toolkit documentation <http://vumi-jssandbox-toolkit.readthedocs.org/>`_
* `Jsbox Toolkit source <https://github.com/praekelt/vumi-jssandbox-toolkit/>`_
* `Jsbox application skeleton <https://github.com/praekelt/go-jsbox-skeleton>`_
* `Q promises <https://github.com/kriskowal/q>`_
* `Javascript <https://developer.mozilla.org/en-US/docs/Web/JavaScript>`_
* `Lodash <https://lodash.com/docs>`_
* `Mocha test framework <http://mochajs.org/>`_

For the mobi interface:

* `localStorage <https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API
>`_
* `Service Workers < https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
>`_
