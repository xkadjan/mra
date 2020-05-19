using System;
using System.Diagnostics;
using System.IO;
using System.Threading;

namespace Controller
{
    internal class SerialCommunicationManager
    {
        private Stream _stream;
        public event MessageReceivedHandler MessageReceived;
        public delegate void MessageReceivedHandler(byte[] connection);
        public string NMEA;
        public bool ENC = false;
        public bool HALL = false;
        public bool PPS = false;
        public bool Waiting = false;
        public bool Working = false;
        private double speed = 0;
        public int M1 = 0;
        public int M2 = 0;
        public int Mspeed = 0;

        System.Diagnostics.Stopwatch stopWatch = new Stopwatch();

        public double Speed { get => speed; set => speed = value; }

        public void Listen(Stream stream)
        {
            Thread readPortThread = new Thread(ReceiveSerialData);
            readPortThread.IsBackground = true;
            readPortThread.Start();
            this._stream = stream;
        }

        public void SetWaitingFalse()
        {
            Waiting = false;
        }

        public void SetWorkingFalse()
        {
            Working = false;
        }

        public void SetHALLFalse()
        {
            HALL = false;
        }

        public void SetENCFalse()
        {
            ENC = false;
        }

        public void SetPPSFalse()
        {
            PPS = false;
        }

        public void Send(byte[] message)
        {
            try
            {
                _stream.Write(message, 0, message.Length);
            }
            catch (NullReferenceException exc)
            {
                Console.WriteLine("Could not send command. Is port open and is serial comms manager listening?");
            }
        }

        private void ReceiveSerialData()
        {
            int bufer = 0;
            try
            {
                // Read serial data from stream and process it.
                while (true)
                {
                    Thread.Sleep(2);
                    byte[] InByte = new byte[1];
                    bufer = _stream.Read(InByte, 0, 1);
                    if (bufer > 0) { 
                    if (InByte[0] == 64) { DefineTypeOfMessage(); } // Start byte "@"
                        else { Console.WriteLine("nenalezen @"); }
                    }
                    else { }
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

        private void DefineTypeOfMessage()
        {
            Thread.Sleep(20);
            byte[] inputBt = new byte[2];
            _stream.Read(inputBt, 0, 2); // Type Byte , kolik znaku ma zprava
            byte[] message = new byte[inputBt[1]];
            _stream.Read(message, 0, inputBt[1]);
            byte[] checkEndByte = new byte[2];
            _stream.Read(checkEndByte, 0, 1);

            switch (inputBt[0])
            {
                case 90:  // Zprava do console  
                    ProcessConsoleMessage();
                    break;
                case 71:  // Data z motoru       ok
                    ProcessMotorsData(message);
                    break;
                case 65:  // Watchdog ok
                    ProcessWathDog();
                    break;
                case 88:  // NMEA   ok
                    NMEA = NMEA + System.Text.Encoding.UTF8.GetString(message);
                    break;
                case 69:  // encoder ok
                    ENC = true;
                    break;
                case 72:  // halovka ok

                    if (stopWatch.IsRunning)
                    {
                        stopWatch.Stop();
                        TimeSpan ts = stopWatch.Elapsed;
                        double obvod = 18.84;

                        double time = ((ts.Seconds * 1000) + (ts.Milliseconds));
                        Speed = (int)((obvod / time) * 3600);
                        stopWatch.Reset();
                    }
                    else
                    {
                        stopWatch.Start();
                    }
                    HALL = true;
                    break;
                case 50:  // PPS ok 
                    PPS = true;

                    break;
                case 57:  // waiting ok
                    Waiting = true;

                    break;
                default:
                    Console.WriteLine("Unknow Message");
                    break;
            }
        }

        private void ProcessWathDog()
        {
            byte[] speed = new byte[] { 0, 0 };
            byte[] bytes = FlightControllerMessage.CreateMessage('D', speed);
            _stream.Write(bytes, 0, bytes.Length);
            Working = true;
            Console.WriteLine("Working");
        }

        private void ProcessMotorsData(byte[] MotorData)
        {
            int M1New = BitConverter.ToInt16(MotorData, 0);
            M1New = (3 * M1)+M1New;
            M1 = (int)(M1New / 4);
            int M2New = BitConverter.ToInt16(MotorData, 2);
            M2New = (3 * M2) + M2New;
            M2 = (int)(M2New / 4);
            Mspeed = BitConverter.ToInt16(MotorData, 4);
        }

        private void ProcessConsoleMessage()
        {          
        }

        private bool CheckSum(byte[] message)
        {
            byte checkSum = message[message.Length - 2];

            if (message[message.Length - 1]==13)
            {
                Console.WriteLine("No end of message");
                return false;
            }
            else
            {
                byte dataSum = 0;
                for(int i =0; i<message.Length-2 ; i++)
                {
                    dataSum = (byte)(dataSum + message[i]);
                }
                if(dataSum == checkSum)
                {
                    return true;
                }
                else
                {
                    Console.WriteLine("Bad checkSum");
                    return false;
                }
            }
        }
    }
}
