# I2C Stress Test App

## Introduction
The I2C Stress Test App is a tool designed to stress test the I2C bus, particularly useful for ADC (Analog-to-Digital Converter) and MCP (Microchip Technology) related operations. Specifically used for a project at work, but wanted to make it public just to showcase some work.

## Installation
1. Make the setup script executable:
    ```
    sudo chmod +x setup.sh
    ```
2. Run the setup script:
    ```
    ./setup.sh
    ```
3. To start the application, type the following in your terminal:
    ```
    i2c-stress-test
    ```

## Usage

### ADC Screen
- **Requests:** Set the number of requests you want to send to the ADC bus within the specified time interval (frequency).
- **Frequency:** Define the time interval (in seconds) in which the set number of requests will be sent.

For example, setting 100 requests at 1 frequency will attempt to send 100 requests per second. Upon starting, a live ADC status page will be displayed, showing ongoing status. The operation is indefinite until either a failure occurs or the "Stop" button is pressed, which then directs you to a results page.

### MCP Screen
- **Pin Delay (milliseconds):** Set the duration to pause between activating each relay.
- **Cycle Delay (seconds):** Set the time to wait between each full sequence of relay activation.

Upon starting, a live MCP status page will be displayed, showing the ongoing status of the test modes specific to VST's "Green Machine." The test runs for a full sequence and can be stopped manually or will stop automatically upon failure, then displaying an MCP results page.
