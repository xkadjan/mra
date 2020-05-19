using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;

namespace HexacopterController
{
    class SerialCommunicationManager
    {
        Stream stream;
        public event MessageReceivedHandler MessageReceived;
        public delegate void MessageReceivedHandler(byte[] connection);

        public void Listen(Stream stream)
        {
            Thread readPortThread = new Thread(receiveSerialData);
            readPortThread.IsBackground = true;
            readPortThread.Start();
            this.stream = stream;
        }

        public void Send(byte[] message)
        {
            try
            {
                stream.Write(message, 0, message.Length);
            }
            catch (NullReferenceException exc)
            {
                Console.WriteLine("Could not send command. Is port open and is serial comms manager listening?");
            }
        }

        private void receiveSerialData()
        {
            // The buffer should at least 2 times the size of the largest possible message.
            byte[] buffer = new byte[2048];
            int firstEmptySpace = 0;
            int availiableSpace = buffer.Length;
            int startOfMessage = 0;
            int endOfMmessage = 0;
            int bytesInBuffer = 0;
            byte sentinel = Convert.ToByte('\r');

            try
            {
                // Read serial data from stream and process it.
                while (true)
                {
                    int numberRead = 1;
                    while (numberRead > 0)
                    {
                        // Fill up the buffer.
                        availiableSpace = buffer.Length - firstEmptySpace;
                        numberRead = stream.Read(buffer, firstEmptySpace, availiableSpace);

                        // Get messages.
                        startOfMessage = 0;
                        bytesInBuffer = firstEmptySpace + numberRead;
                        for (int i = 0; i < bytesInBuffer; i++)
                        {
                            // If a sentinel was found signaling the end of a message.
                            if (buffer[i] == sentinel)
                            {
                                endOfMmessage = i;
                                byte[] message = new byte[endOfMmessage - startOfMessage + 1];
                                Buffer.BlockCopy(buffer, startOfMessage, message, 0, message.Length);
                                startOfMessage = endOfMmessage + 1;

                                // If an event handler has been assigned, call it.
                                if (MessageReceived != null)
                                {
                                    MessageReceived(message);
                                }
                            }
                        }

                        // Copy any remaining bytes to the start of the buffer.
                        Buffer.BlockCopy(buffer, startOfMessage, buffer, 0, bytesInBuffer - startOfMessage);
                        firstEmptySpace = bytesInBuffer - startOfMessage;
                    }
                }
            }
            catch (NullReferenceException exc)
            {
                Console.WriteLine("Serial communicator is not listening. Was port opened?");
            }
            catch (TimeoutException exc)
            {
                Console.WriteLine("Serial communication timed out.");
            }
            catch (IOException exc)
            {
                Console.WriteLine("Serial communicator is no longer listening.");
            }
        }
    }
}
