using System.Text;
using System.IO;
using System.Windows.Forms;

namespace Controller
{
    internal class ConsoleWriter : StringWriter
    {
        private readonly int _capacity;
        private readonly TextBox _box;
        private readonly StringBuilder _builder;

        // is the text box blinking a lot? reduce the capacity
        public ConsoleWriter(TextBox box, int capacity)
        {
            this._capacity = capacity;
            this._box = box;
            _builder = this.GetStringBuilder();
        }

        private void UpdateTextBox()
        {
            // pretty sure this is not very efficient
            if (_builder.Length > _capacity)
                _builder.Remove(0, _builder.Length - _capacity);
            MainForm.SetControlPropertyThreadSafe(_box, "Text", this.ToString());
            MainForm.SetControlPropertyThreadSafe(_box, "SelectionStart", _box.Text.Length);
            MainForm.CallControlFunctionThreadSafe(_box, "ScrollToCaret");
        }

        public override void Write(bool value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(char[] buffer)
        {
            base.Write(buffer);
            UpdateTextBox();
        }

        public override void Write(decimal value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(char value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(char[] buffer, int index, int count)
        {
            base.Write(buffer, index, count);
            UpdateTextBox();
        }

        public override void Write(double value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(float value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(int value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(long value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(object value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(string format, object arg0)
        {
            base.Write(format, arg0);
            UpdateTextBox();
        }

        public override void Write(string format, object arg0, object arg1)
        {
            base.Write(format, arg0, arg1);
            UpdateTextBox();
        }

        public override void Write(string format, object arg0, object arg1, object arg2)
        {
            base.Write(format, arg0, arg1, arg2);
            UpdateTextBox();
        }

        public override void Write(string format, params object[] arg)
        {
            base.Write(format, arg);
            UpdateTextBox();
        }

        public override void Write(string value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(uint value)
        {
            base.Write(value);
            UpdateTextBox();
        }

        public override void Write(ulong value)
        {
            base.Write(value);
            UpdateTextBox();
        }
    }
}
