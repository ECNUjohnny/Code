#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <fstream>
using namespace std;
#define MemSize 1000 // memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

struct IFStruct
{
    bitset<32> PC;
    bool nop;
};

struct IDStruct
{
    bitset<32> Instr;
    bool nop;
};

struct EXStruct
{
    bitset<32> Read_data1;
    bitset<32> Read_data2;
    bitset<16> Imm;
    bitset<5> Rs;
    bitset<5> Rt;
    bitset<5> Wrt_reg_addr;
    bool is_I_type;
    bool rd_mem;
    bool wrt_mem;
    bool alu_op; // 1 for addu, lw, sw, 0 for subu
    bool wrt_enable;
    bool nop;
};

struct MEMStruct
{
    bitset<32> ALUresult;
    bitset<32> Store_data;
    bitset<5> Rs;
    bitset<5> Rt;
    bitset<5> Wrt_reg_addr;
    bool rd_mem;
    bool wrt_mem;
    bool wrt_enable;
    bool nop;
};

struct WBStruct
{
    bitset<32> Wrt_data;
    bitset<5> Rs;
    bitset<5> Rt;
    bitset<5> Wrt_reg_addr;
    bool wrt_enable;
    bool nop;
};

struct stateStruct
{
    IFStruct IF;
    IDStruct ID;
    EXStruct EX;
    MEMStruct MEM;
    WBStruct WB;
};

class RF
{
public:
    bitset<32> Reg_data;

    RF()
    {
        Registers.resize(32);
        Registers[0] = bitset<32>(0);
    }

    bitset<32> readRF(bitset<5> Reg_addr)
    {
        Reg_data = Registers[Reg_addr.to_ulong()];
        return Reg_data;
    }

    void writeRF(bitset<5> Reg_addr, bitset<32> Wrt_reg_data)
    {
        Registers[Reg_addr.to_ulong()] = Wrt_reg_data;
    }

    void outputRF()
    {
        ofstream rfout;
        rfout.open("RFresult.txt", std::ios_base::app);
        if (rfout.is_open())
        {
            rfout << "State of RF:\t" << endl;
            for (int j = 0; j < 32; j++)
            {
                rfout << Registers[j] << endl;
            }
        }
        else
            cout << "Unable to open file";
        rfout.close();
    }

private:
    vector<bitset<32>> Registers;
};

class INSMem
{
public:
    bitset<32> Instruction;
    INSMem()
    {
        IMem.resize(MemSize);
        ifstream imem;
        string line;
        int i = 0;
        imem.open("imem.txt");
        if (imem.is_open())
        {
            while (getline(imem, line))
            {
                IMem[i] = bitset<8>(line);
                i++;
            }
        }
        else
            cout << "Unable to open file";
        imem.close();
    }

    bitset<32> readInstr(bitset<32> ReadAddress)
    {
        string insmem;
        insmem.append(IMem[ReadAddress.to_ulong()].to_string());
        insmem.append(IMem[ReadAddress.to_ulong() + 1].to_string());
        insmem.append(IMem[ReadAddress.to_ulong() + 2].to_string());
        insmem.append(IMem[ReadAddress.to_ulong() + 3].to_string());
        Instruction = bitset<32>(insmem); // read instruction memory
        return Instruction;
    }

private:
    vector<bitset<8>> IMem;
};

class DataMem
{
public:
    bitset<32> ReadData;
    DataMem()
    {
        DMem.resize(MemSize);
        ifstream dmem;
        string line;
        int i = 0;
        dmem.open("dmem.txt");
        if (dmem.is_open())
        {
            while (getline(dmem, line))
            {
                DMem[i] = bitset<8>(line);
                i++;
            }
        }
        else
            cout << "Unable to open file";
        dmem.close();
    }

    bitset<32> readDataMem(bitset<32> Address)
    {
        string datamem;
        datamem.append(DMem[Address.to_ulong()].to_string());
        datamem.append(DMem[Address.to_ulong() + 1].to_string());
        datamem.append(DMem[Address.to_ulong() + 2].to_string());
        datamem.append(DMem[Address.to_ulong() + 3].to_string());
        ReadData = bitset<32>(datamem); // read data memory
        return ReadData;
    }

    void writeDataMem(bitset<32> Address, bitset<32> WriteData)
    {
        DMem[Address.to_ulong()] = bitset<8>(WriteData.to_string().substr(0, 8));
        DMem[Address.to_ulong() + 1] = bitset<8>(WriteData.to_string().substr(8, 8));
        DMem[Address.to_ulong() + 2] = bitset<8>(WriteData.to_string().substr(16, 8));
        DMem[Address.to_ulong() + 3] = bitset<8>(WriteData.to_string().substr(24, 8));
    }

    void outputDataMem()
    {
        ofstream dmemout;
        dmemout.open("dmemresult.txt");
        if (dmemout.is_open())
        {
            for (int j = 0; j < 1000; j++)
            {
                dmemout << DMem[j] << endl;
            }
        }
        else
            cout << "Unable to open file";
        dmemout.close();
    }

private:
    vector<bitset<8>> DMem;
};

void printState(stateStruct state, int cycle)
{
    ofstream printstate;
    printstate.open("stateresult.txt", std::ios_base::app);
    if (printstate.is_open())
    {

        printstate << "State after executing cycle:\t" << cycle << endl;

        printstate << "IF.PC:\t" << state.IF.PC.to_ulong() << endl;
        printstate << "IF.nop:\t" << state.IF.nop << endl;

        printstate << "ID.Instr:\t" << state.ID.Instr << endl;
        printstate << "ID.nop:\t" << state.ID.nop << endl;

        printstate << "EX.Read_data1:\t" << state.EX.Read_data1 << endl;
        printstate << "EX.Read_data2:\t" << state.EX.Read_data2 << endl;
        printstate << "EX.Imm:\t" << state.EX.Imm << endl;
        printstate << "EX.Rs:\t" << state.EX.Rs << endl;
        printstate << "EX.Rt:\t" << state.EX.Rt << endl;
        printstate << "EX.Wrt_reg_addr:\t" << state.EX.Wrt_reg_addr << endl;
        printstate << "EX.is_I_type:\t" << state.EX.is_I_type << endl;
        printstate << "EX.rd_mem:\t" << state.EX.rd_mem << endl;
        printstate << "EX.wrt_mem:\t" << state.EX.wrt_mem << endl;
        printstate << "EX.alu_op:\t" << state.EX.alu_op << endl;
        printstate << "EX.wrt_enable:\t" << state.EX.wrt_enable << endl;
        printstate << "EX.nop:\t" << state.EX.nop << endl;

        printstate << "MEM.ALUresult:\t" << state.MEM.ALUresult << endl;
        printstate << "MEM.Store_data:\t" << state.MEM.Store_data << endl;
        printstate << "MEM.Rs:\t" << state.MEM.Rs << endl;
        printstate << "MEM.Rt:\t" << state.MEM.Rt << endl;
        printstate << "MEM.Wrt_reg_addr:\t" << state.MEM.Wrt_reg_addr << endl;
        printstate << "MEM.rd_mem:\t" << state.MEM.rd_mem << endl;
        printstate << "MEM.wrt_mem:\t" << state.MEM.wrt_mem << endl;
        printstate << "MEM.wrt_enable:\t" << state.MEM.wrt_enable << endl;
        printstate << "MEM.nop:\t" << state.MEM.nop << endl;

        printstate << "WB.Wrt_data:\t" << state.WB.Wrt_data << endl;
        printstate << "WB.Rs:\t" << state.WB.Rs << endl;
        printstate << "WB.Rt:\t" << state.WB.Rt << endl;
        printstate << "WB.Wrt_reg_addr:\t" << state.WB.Wrt_reg_addr << endl;
        printstate << "WB.wrt_enable:\t" << state.WB.wrt_enable << endl;
        printstate << "WB.nop:\t" << state.WB.nop << endl;

        puts("");
    }
    else
        cout << "Unable to open file";
    printstate.close();
}

int main()
{

    RF myRF;
    INSMem myInsMem;
    DataMem myDataMem;
    struct stateStruct state{0};
    state.IF.nop = false;
    state.ID.nop = true;
    state.EX.nop = true;
    state.MEM.nop = true;
    state.WB.nop = true;
    state.EX.alu_op = true;
    int cycle = 0;

    while (1)
    {
        
        stateStruct newState = state; // 初始化 newState 继承当前状态（防止未赋值的字段丢失）

        /* --------------------- WB stage --------------------- */
        if (!state.WB.nop) {
            // 如果写使能有效且目标寄存器不为 0（RISC-V 中 x0 恒为 0）
            if (state.WB.wrt_enable && state.WB.Wrt_reg_addr.to_ulong() != 0) {
                myRF.writeRF(state.WB.Wrt_reg_addr, state.WB.Wrt_data);
            }
        }

        /* --------------------- MEM stage --------------------- */
        if (!state.MEM.nop) {
            
            if (state.MEM.rd_mem) {
                newState.WB.Wrt_data = myDataMem.readDataMem(state.MEM.ALUresult);
            } else {
                newState.WB.Wrt_data = state.MEM.ALUresult;
            }

            
            if (state.MEM.wrt_mem) {
                myDataMem.writeDataMem(state.MEM.ALUresult, state.MEM.Store_data);
            }

            
            newState.WB.Rs = state.MEM.Rs;
            newState.WB.Rt = state.MEM.Rt;
            newState.WB.Wrt_reg_addr = state.MEM.Wrt_reg_addr;
            newState.WB.wrt_enable = state.MEM.wrt_enable;
        }
        newState.WB.nop = state.MEM.nop;

        /* --------------------- EX stage --------------------- */
        if (!state.EX.nop) {
            bitset<32> op1 = state.EX.Read_data1;
            bitset<32> op2;

            if (state.EX.is_I_type || state.EX.rd_mem || state.EX.wrt_mem) {
                string imm_str = state.EX.Imm.to_string();
                
                if (imm_str[0] == '1') {
                    op2 = bitset<32>(string(16, '1') + imm_str);
                } else {
                    op2 = bitset<32>(string(16, '0') + imm_str);
                }
            } else {
                op2 = state.EX.Read_data2;
            }

            
            if (state.EX.alu_op) { 
                // 1 为 add, addi, ld, sd
                newState.MEM.ALUresult = bitset<32>(op1.to_ulong() + op2.to_ulong());
            } else { 
                // 0 为 sub
                newState.MEM.ALUresult = bitset<32>(op1.to_ulong() - op2.to_ulong());
            }

            newState.MEM.Store_data = state.EX.Read_data2;
            newState.MEM.Rs = state.EX.Rs;
            newState.MEM.Rt = state.EX.Rt;
            newState.MEM.Wrt_reg_addr = state.EX.Wrt_reg_addr;
            newState.MEM.rd_mem = state.EX.rd_mem;
            newState.MEM.wrt_mem = state.EX.wrt_mem;
            newState.MEM.wrt_enable = state.EX.wrt_enable;
        }
        newState.MEM.nop = state.EX.nop;

        /* --------------------- ID stage --------------------- */
        bool branch_taken = false;
        bitset<32> branch_target;

        if (!state.ID.nop) {
    
            if (state.ID.Instr.to_ulong() == 0xffffffff) {
                newState.EX.nop = true;
                
               
                newState.EX.Rs = bitset<5>(0);
                newState.EX.Rt = bitset<5>(0);
                newState.EX.Wrt_reg_addr = bitset<5>(0);
                newState.EX.wrt_enable = false;
                newState.EX.rd_mem = false;
                newState.EX.wrt_mem = false;
                newState.EX.is_I_type = false;
                newState.EX.alu_op = true;
            } else {
                string instr_str = state.ID.Instr.to_string();
                
                
                string opcode = instr_str.substr(25, 7);
                string func3  = instr_str.substr(17, 3);
                string func7  = instr_str.substr(0, 7);

                bool is_R      = (opcode == "0110011");
                bool is_I      = (opcode == "0010011"); 
                bool is_load   = (opcode == "0000011"); 
                bool is_store  = (opcode == "0100011"); 
                bool is_branch = (opcode == "1100011"); 

                bitset<5> rs1(instr_str.substr(12, 5));
                bitset<5> rs2(instr_str.substr(7, 5));
                bitset<5> rd(instr_str.substr(20, 5));

                if (rs1 == state.EX.Wrt_reg_addr) newState.EX.Read_data1 = state.MEM.ALUresult;
                else newState.EX.Read_data1 = myRF.readRF(rs1);

                if (rs2 == state.EX.Wrt_reg_addr) newState.EX.Read_data2 = state.MEM.ALUresult;
                else newState.EX.Read_data2 = myRF.readRF(rs2);

                // newState.EX.Read_data1 = myRF.readRF(rs1);
                // newState.EX.Read_data2 = myRF.readRF(rs2);

                string imm_12;
                if (is_load || is_I) {
                    imm_12 = instr_str.substr(0, 12);
                } else if (is_store) {
                    imm_12 = instr_str.substr(0, 7) + instr_str.substr(20, 5);
                } else {
                    imm_12 = "000000000000";
                }

               
                if (imm_12[0] == '1') {
                    newState.EX.Imm = bitset<16>(string(4, '1') + imm_12);
                } else {
                    newState.EX.Imm = bitset<16>(string(4, '0') + imm_12);
                }

             
                newState.EX.Rs = rs1;
                newState.EX.Rt = rs2;
                newState.EX.Wrt_reg_addr = rd;
                newState.EX.is_I_type = is_I;
                newState.EX.rd_mem = is_load;
                newState.EX.wrt_mem = is_store;
                newState.EX.wrt_enable = (is_R || is_I || is_load);

                if (is_R && func3 == "000" && func7 == "0100000") {
                    newState.EX.alu_op = false; // sub
                } else {
                    newState.EX.alu_op = true;  // add, addi, ld, sd
                }

                
                if (is_branch && (newState.EX.Read_data1 != newState.EX.Read_data2)) { 
                    branch_taken = true;
                    string b_imm = string(1, instr_str[0]) + string(1, instr_str[24]) + instr_str.substr(1, 6) + instr_str.substr(20, 4) + "0";
                    bitset<32> offset;
                    
                    if (b_imm[0] == '1') offset = bitset<32>(string(19, '1') + b_imm);
                    else offset = bitset<32>(string(19, '0') + b_imm);

                    
                    branch_target = bitset<32>(state.IF.PC.to_ulong() - 4 + offset.to_ulong());
                }
            }
        }
        newState.EX.nop = state.ID.nop;

        /* --------------------- IF stage --------------------- */
        if (!state.IF.nop) {
            bitset<32> instruction = myInsMem.readInstr(state.IF.PC);
            
            
            if (instruction.to_ulong() == 0xffffffff) {
                newState.IF.nop = true;   
                newState.ID.nop = false;  
                newState.ID.Instr = instruction;
                newState.IF.PC = state.IF.PC; 
            } else {
                newState.IF.nop = false; 
                
                
                if (branch_taken) {
                    newState.ID.nop = true; 
                    newState.IF.PC = branch_target; 
                } else {
                    newState.ID.nop = false;
                    newState.ID.Instr = instruction;
                    newState.IF.PC = bitset<32>(state.IF.PC.to_ulong() + 4); // 正常 PC+4
                }
            }
        } else {
            
            newState.IF.nop = true;
            newState.ID.nop = true;
            newState.IF.PC = state.IF.PC; 
        }

        /* --------------------- Stall unit--------------------- */
        

        if (state.IF.nop && state.ID.nop && state.EX.nop && state.MEM.nop && state.WB.nop)
            break;

        printState(newState, cycle); // print states after executing cycle 0, cycle 1, cycle 2 ...

        cycle += 1;
        state = newState; /*The end of the cycle and updates the current state with the values calculated in this cycle */
    }

    myRF.outputRF();           // dump RF;
    myDataMem.outputDataMem(); // dump data mem

    return 0;
}