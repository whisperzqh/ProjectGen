import hl7
from hl7 import Accessor, Component, Field, Message, ParseException, Repetition, Segment

from datetime import datetime
from hl7 import parse_datetime

import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import create_autospec
import hl7.mllp

sample_hl7 = "\r".join(
    [
        "MSH|^~\\&|CITY HOSPITAL|LABSYS|REGIONAL CLINIC|MAIN CAMPUS|202510151420||ORU^R01|MSGID98765|P|2.4",
        "PID|||987-65-4321||SMITH^JOHN^A^^^^L|DOE|19850712|M|||456 OAK STREET^^SPRINGFIELD^IL^62704||(312)555-0198|(312)555-0177||||HN987654321||88-B7721^IL^20240310",
        "OBR|1|REQ778899^REGIONAL CLINIC|SPEC20251015^CITY HOSP LAB|2951-2^CHOLESTEROL, TOTAL|||202510151000||||||||999-88-7777^WILSON^ROBERT T^^^^MD^^CITY MEDICAL GROUP|||||||||F||||||111-22-3333^GALVANI^LUIGI^^^^MD",
        "OBX|1|NM|2951-2^CHOLESTEROL, TOTAL^MCNC:PT:SER/PLAS:QN||210|mg/dL|<200|H|||F",
        "OBX|2|NM|2093-3^HDL CHOLESTEROL^MCNC:PT:SER/PLAS:QN||55|mg/dL|>40|N|||F\r",
    ]
)

sample_file = "\r".join(
    [
        "FHS|^~\\&||WESTCLINIC||MEDNET|20251015142530|||westclinic_20251015.hl7|",
        "BHS|^~\\&||WESTCLINIC||MEDNET|20251015142530||||batch_20251015_001",
        "MSH|^~\\&||WESTCLINIC||MEDNET|20251015142000||ADT^A08^ADT_A01|MSG987654321|P|2.5|||AL|AL|US|UTF-8",
        "EVN|A08|20251015140000",
        "PID|1||9876543210^^^200^MR||JOHNSON^EMILY^R^^^^L||19900517|F|||789 MAPLE AVE^^BOSTON^MA^02101||||6175550142||||||||2200|||||||||BBB",
        "PD1||3",
        "NK1|1||2||||||||||||||||||3",
        "PV1|1|I||||^^^^^5",
        "BTS|1",
        "FTS|1",
        "",
    ]
)

rep_sample_hl7 = "\r".join(
    [
        "MSH|^~\\&|CITY MED LAB|LABSYS-V2|REGIONAL HOSP|EAST WING|20251015143000||ORU^R01|MSG-889900|P|2.4",
        "PID|RecordID|Alpha^Beta|Gamma^Delta&Epsilon^Zeta|ItemA~ItemB",
        "",
    ]
)

sample_batch = "\r".join(
    [
        "BHS|^~\\&||WESTERN MEDICAL||HEALTHNET|20251015160000||||WM20251015_BATCH_01",
        "MSH|^~\\&||WESTERN MEDICAL||HEALTHNET|20251015155500||ADT^A08^ADT_A01|WM_MSG_778899|P|2.5|||AL|AL|US|UTF-8",
        "EVN|A08|20251015153000",
        "PID|1||MRN88990011^^^300^MR||DAVIS^SARAH^L^^^^L||19881205|F|||321 CEDAR BLVD^^PORTLAND^OR^97205||||5035550189||||||||3300|||||||||CCC",
        "PD1||5",
        "NK1|1||3||||||||||||||||||1",
        "PV1|1|I||||^^^^^8",
        "BTS|1",
        "",
    ]
)

def test_parse_new():
    """Newly constructed test"""

    msg = hl7.parse(sample_hl7)
    assert len(msg) == 5
    assert isinstance(msg[0][0][0], str)
    assert msg[0][0][0] == "MSH"
    assert msg[3][0][0] == "OBX"
    assert msg[3][3] == [[["2951-2"], ["CHOLESTEROL, TOTAL"], ["MCNC:PT:SER/PLAS:QN"]]]
    assert msg[0][1][0] == "|"
    assert isinstance(msg[0][1], hl7.Field)
    assert msg[0][2][0] == r"^~\&"
    assert isinstance(msg[0][2], hl7.Field)
    assert msg[0][9] == [[["ORU"], ["R01"]]]
    assert str(msg) == sample_hl7
    assert str(msg) == sample_hl7

def test_parse_file():
    """Newly constructed test"""

    file = hl7.parse_file(sample_file)
    assert len(file) == 1
    assert isinstance(file[0], hl7.Batch)
    assert isinstance(file.header, hl7.Segment)
    assert file.header[0][0] == "FHS"
    assert file.header[4][0] == "WESTCLINIC"
    assert isinstance(file.trailer, hl7.Segment)
    assert file.trailer[0][0] == "FTS"
    assert file.trailer[1][0] == "1"

def test_extract_new():
    """Newly constructed test"""

    msg = hl7.parse(rep_sample_hl7)

    assert msg["PID.3.1.2.2"] == "Epsilon"
    assert msg[Accessor("PID", 1, 3, 1, 2, 2)] == "Epsilon"

    assert msg["PID.1.1"] == "RecordID"
    assert msg[Accessor("PID", 1, 1, 1)] == "RecordID"
    assert msg["PID.1"] == "RecordID"
    assert msg["PID1.1"] == "RecordID"
    assert msg["PID.3.1.2"] == "Delta"

    assert msg["PID.1.1.1.1"] == "RecordID"

    try:
        msg.extract_field(*Accessor.parse_key("PID.1.1.1.2"))
        assert False, "Expected IndexError"
    except IndexError as e:
        assert "PID.1.1.1.2" in str(e)

    assert msg["MSH.20"] == ""

    assert msg["PID.3.1.2.3"] == ""
    assert msg["PID.3.1.3"] == "Zeta"
    assert msg["PID.3.1.4"] == ""

def test_assign_new_alt():
    """Newly constructed test"""

    msg = hl7.parse(rep_sample_hl7)

    msg["PID.3.1.2.2"] = "UPDATED_LAMBDA"
    assert msg["PID.3.1.2.2"] == "UPDATED_LAMBDA"

    msg["PID.3.1.2.3"] = "NEW_SUB_X"
    assert msg["PID.3.1.2.3"] == "NEW_SUB_X"

    msg2 = hl7.parse(str(msg))
    assert msg2["PID.3.1.2.2"] == "UPDATED_LAMBDA"
    assert msg2["PID.3.1.2.3"] == "NEW_SUB_X"

def test_parse_batch_new():
    """Newly constructed test"""

    batch = hl7.parse_batch(sample_batch)
    
    assert len(batch) == 1
    assert isinstance(batch[0], hl7.Message)
    assert isinstance(batch.header, hl7.Segment)
    assert batch.header[0][0] == "BHS"
    assert batch.header[4][0] == "WESTERN MEDICAL"
    assert isinstance(batch.trailer, hl7.Segment)
    assert batch.trailer[0][0] == "BTS"
    assert batch.trailer[1][0] == "1"

def test_create_parse_plan_new():
    """Newly constructed test"""

    plan = hl7.parser.create_parse_plan(sample_hl7)

    assert plan.separators == "\r|~^&"
    assert plan.containers == [Message, Segment, Field, Repetition, Component]

def test_unicode():
    """Newly constructed test"""

    msg = hl7.parse(sample_hl7)
    assert str(msg) == sample_hl7
    assert str(msg[3][3]) == "2951-2^CHOLESTEROL, TOTAL^MCNC:PT:SER/PLAS:QN"

def test_parse_datetime_frac_new():
    """Newly constructed test"""

    assert parse_datetime("20251015163045.2") == datetime(2025, 10, 15, 16, 30, 45, 200000)
    assert parse_datetime("20251015163045.03") == datetime(2025, 10, 15, 16, 30, 45, 30000)
    assert parse_datetime("20251015163045.004") == datetime(2025, 10, 15, 16, 30, 45, 4000)
    assert parse_datetime("20251015163045.0005") == datetime(2025, 10, 15, 16, 30, 45, 500)

def test_escape_new():
    """Newly constructed test"""

    msg = hl7.parse(rep_sample_hl7)

    assert msg.escape("\\") == "\\E\\"
    assert msg.escape("|") == "\\F\\"
    assert msg.escape("^") == "\\S\\"
    assert msg.escape("&") == "\\T\\"
    assert msg.escape("~") == "\\R\\"

    assert msg.escape("asdf") == "asdf"

    assert msg.escape("áéíóú") == "\\Xe1\\\\Xe9\\\\Xed\\\\Xf3\\\\Xfa\\"
    assert msg.escape("äsdf") == "\\Xe4\\sdf"

START_BLOCK = b"\x0b"
END_BLOCK = b"\x1c"
CARRIAGE_RETURN = b"\x0d"


class MLLPStreamWriterTest(IsolatedAsyncioTestCase):
    """Newly constructed test"""

    def setUp(self):
        self.transport = create_autospec(asyncio.Transport)

    async def asyncSetUp(self):
        self.writer = hl7.mllp.MLLPStreamWriter(
            self.transport,
            create_autospec(asyncio.streams.StreamReaderProtocol),
            create_autospec(hl7.mllp.MLLPStreamReader),
            asyncio.get_running_loop(),
        )

    def test_writeblock(self):
        test_payload = b"MSH|^~\\&|LAB|HOSP|...||ORU^R01|12345|P|2.4\rOBX|1|NM|2951-2^CHOL||210|mg/dL"
        
        self.writer.writeblock(test_payload)
        
        expected = START_BLOCK + test_payload + END_BLOCK + CARRIAGE_RETURN
        self.transport.write.assert_called_once_with(expected)