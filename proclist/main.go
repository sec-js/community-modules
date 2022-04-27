//go:build windows || linux || darwin

package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	//"path/filepath"
	"sort"
	"strings"
    "strconv"

	"github.com/alexeyco/simpletable"
	"github.com/shirou/gopsutil/process"
)

type ServerRequest struct {
	Name   string `json:"name,omitempty"`
	PID    string  `json:"pid,omitempty,string`
	PPID   string  `json:"ppid,omitempty,string`
	User   string `json:"user,omitempty,"`
	Format string `json:"format,omitempty"`
}

type HostProcs struct {
	Name       string   `json:"name,omitempty"`
	PID        int32    `json:"pid,omitempty"`
	PPID       int32    `json:"ppid,omitempty"`
	Mem        float32  `json:"memory,omitempty"`
	Nice       int32    `json:"nice,omitempty"`
	Priority   int32    `json:"priority,omitempty"`
	CPU        float64  `json:"cpu,omitempty"`
	User       string   `json:"user,omitempty"`
	Cwd        string   `json:"cwd,omitempty"`
	Env        []string `json:"env,omitempty"`
	Cmdline    string   `json:"cmdline,omitempty"`
	CreateTime int64    `json:"createtime,omitempty"`
	Exe        string   `json:"exe,omitempty"`
}

const (
	CATEGORY_NONE                 int = 0
	CATEGORY_INPUT_COMMUNICATION      = 1
	CATEGORY_OUTPUT_COMMUNICATION     = 2
	CATEGORY_WORKER                   = 4
)

const (
	SCYTHE_NOERROR                   int = 0
	SCYTHE_ERROR_INTERNAL                = 1
	SCYTHE_ERROR_NOT_FOUND               = 2
	SCYTHE_ERROR_NOT_ALLOWED             = 5
	SCYTHE_ERROR_OUTOFMEMORY             = 14
	SCYTHE_ERROR_INVALID_PARAMETER       = 87
	SCYTHE_ERROR_ALREADY_RUNNING         = 183
	SCYTHE_BERROR_FILE_TOO_LARGE         = 223
	SCYTHE_ERROR_DATA_CHECKSUM_ERROR     = 323
)

type ScytheMessageType struct {
	messageID             []byte
	flags                 uint32
	context               uint64
	sourceModuleID        []byte
	destinationModuleID   []byte
	destinationModuleType uint32
	content               []byte
}

var moduleID []byte = []byte{0x9A, 0xEC, 0xCA, 0x51, 0x6F, 0x60, 0x41, 0xC5, 0x98, 0x95, 0x9C, 0x28, 0x9B, 0x42, 0xDC, 0xA8}
var moduleType int = CATEGORY_WORKER
var moduleVersion float32 = 1.0

func module_init() int {
	return SCYTHE_NOERROR
}

func module_deinit() int {
	return SCYTHE_NOERROR
}

func module_run(message ScytheMessageType) int {
	response := message
	response.destinationModuleID = message.sourceModuleID
	response.destinationModuleType = CATEGORY_OUTPUT_COMMUNICATION
    //fmt.Printf("Data %s", message.content)
	response.content = parseRequest(string(message.content))
    //fmt.Printf("Request: %s\n", message.content)
    //fmt.Println("Inside run func")
	
    return PostMessage(response)
}


func backwards(inbytes []byte) []byte {
	outbytes := inbytes
	for i, j := 0, len(outbytes)-1; i < j; i, j = i+1, j-1 {
		outbytes[i], outbytes[j] = outbytes[j], outbytes[i]
	}
	return outbytes
}


func ListProcess() []HostProcs {
	var procs []HostProcs
	pids, err := process.Pids()
	if err != nil {
		fmt.Printf("Error: %v", err)
	}
	for _, p := range pids {
		pid, _ := process.NewProcess(p)
		name, _ := pid.Name()
		nice, _ := pid.Nice()
		priority, _ := pid.IOnice()
		mem, _ := pid.MemoryPercent()
		cpu, _ := pid.CPUPercent()
		ppid, _ := pid.Ppid()
		user, _ := pid.Username()
		cwd, _ := pid.Cwd()
		env, _ := pid.Environ()
		exe, _ := pid.Exe()
		cmdline, _ := pid.Cmdline()
		createtime, _ := pid.CreateTime()
		pcs := HostProcs{Name: name,
			PID:        p,
			PPID:       ppid,
			Nice:       nice,
			Priority:   priority,
			Mem:        mem,
			CPU:        cpu,
			Cwd:        cwd,
			Env:        env,
			Cmdline:    cmdline,
			CreateTime: createtime,
			Exe:        exe,
			User:       user,
		}
		procs = append(procs, pcs)
	}
	return procs
}

func reverseSortUser(procs []HostProcs) {
	sort.Slice(procs, func(i, j int) bool {
		return procs[i].User > procs[j].User
	})
}

func sortByUser(procs []HostProcs) {
	sort.Slice(procs, func(i, j int) bool {
		return procs[i].User < procs[j].User
	})
}

// Find all processes running for a given User
func filterByUser(procs []HostProcs, user string) []HostProcs {
	var filterProcs []HostProcs
	for _, p := range procs {
		if p.User == user {
			filterProcs = append(filterProcs, p)
		}
	}
	return filterProcs
}

// Find a specific PID
func filterByPID(procs []HostProcs, pid int32) []HostProcs {
	var filterProcs []HostProcs
	for _, p := range procs {
		if p.PID == pid {
			filterProcs = append(filterProcs, p)
		} //end
	} //end
	return filterProcs
} //emd

// Lazy Match a specific process(es) by name
func filterByName(procs []HostProcs, name string) []HostProcs {
	var filterProcs []HostProcs
	for _, p := range procs {
		if strings.Contains(strings.ToLower(p.Name), strings.ToLower(name)) {
			filterProcs = append(filterProcs, p)
		}
	}
	return filterProcs
} //end

// Find all processes with Parent Process ID
func fitlerByPPID(procs []HostProcs, ppid int32) []HostProcs {
	var filterProcs []HostProcs
	for _, p := range procs {
		if p.PPID == ppid {
			filterProcs = append(filterProcs, p)
		}
	} //end
	return filterProcs
}

//Print General Table
func printTable(procs []HostProcs) string {
	tbl := simpletable.New()
	if len(procs) == 0 {
		return "[!] No Processes Found!"
	} else {
		tbl.Header = &simpletable.Header{
			Cells: []*simpletable.Cell{
				{Align: simpletable.AlignLeft, Text: "PID"},
				{Align: simpletable.AlignLeft, Text: "Name"},
				{Align: simpletable.AlignLeft, Text: "PPID"},
				{Align: simpletable.AlignLeft, Text: "USER"},
				//{Align: simpletable.AlignLeft, Text: "EXE"},
				//{Align: simpletable.AlignLeft, Text: "Env"},
			},
		}
		for _, row := range procs {

			r := []*simpletable.Cell{
				{Align: simpletable.AlignLeft, Text: fmt.Sprintf("%d", row.PID)},
				{Align: simpletable.AlignLeft, Text: row.Name},
				{Align: simpletable.AlignLeft, Text: fmt.Sprintf("%d", row.PPID)},
				{Align: simpletable.AlignCenter, Text: row.User},
            	//{Align: simpletable.AlignLeft, Text: filepath.Base(row.Exe)},
				//{Align: simpletable.AlignLeft, Text: fmt.Sprintf("%s", row.Env)},
			}
			tbl.Body.Cells = append(tbl.Body.Cells, r)
		}
	} //end
	return tbl.String()
}

// Simple way to check if int32 values  have been set without dealing with poitners yuck!
func (req *ServerRequest) fill_defaults(){
	req.Name="";
	req.PID="-1";
	req.PPID="-1";
	req.User = "";
    req.Format = "json"
}

// Encode struct []HostProcs into JSON Array and return as []byte arrary
func encodeForTransport(procs []HostProcs) []byte {
	reqBodyBytes := new(bytes.Buffer)
	json.NewEncoder(reqBodyBytes).Encode(procs)
	return reqBodyBytes.Bytes()
}

//Parse incoming request from SCYTHE Server
func parseRequest(data string) []byte {
	var sReq ServerRequest
	sReq.fill_defaults() // hack to allow us to check if value is somethign absurd and hasn't been set. 
	err := json.Unmarshal([]byte(data), &sReq)
	if err != nil {
		errResp := fmt.Sprintf("[!] Error on implant side while decoding Server Request: %v, %v", data, err)
		return []byte(errResp)
	}
	procs := ListProcess() 
	if sReq.PID != "-1"{
		// return all procs by PID
        pid,_ := strconv.Atoi(sReq.PID)
        PID := int32(pid)
		procs = filterByPID(procs,PID)
	} 
	if sReq.PPID != "-1"{
		// return all procs with PPID
        ppid,_ := strconv.Atoi(sReq.PPID)
	    PPID := int32(ppid)	
        procs = filterByPID(procs,PPID)
	}
	if sReq.Name != ""{
		// return all procs with name
		procs = filterByName(procs,sReq.Name)
	}
	if sReq.User != ""{
		// return all procs for user
		procs = filterByUser(procs, sReq.User)
	}
	// If All 4 fields are set, then this will drill down from PID -> PPID -> NAME -> USER, which may very well return nothing. 
	if len(procs) == 0 {
		resp := fmt.Sprintf("[!] No process(es) found for following filtered params (%s,%s,%s,%s)", sReq.PID, sReq.PPID, sReq.Name ,sReq.User)
		return []byte(resp)
	}
	if sReq.Format == "table" {
		return []byte(printTable(procs))
	}
 	return encodeForTransport(procs)
}

func main() {}

