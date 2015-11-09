package main

import (
    "github.com/bradfitz/gomemcache/memcache"
    "fmt"
    "net/http"
    "io/ioutil"
    "encoding/json"
    "encoding/binary"
    "net"
    "bytes"
    "strconv"
    "time"
)

const (
    //URL_APPIDS = "http://222.186.49.42:3737/getallreleaseapp/?new"
    URL_APPIDS = "http://127.0.0.1:3737/getallreleaseapp/?new"
    HOST_MEMCACHED = "127.0.0.1:11211"
    HOST_STATI = "58.215.46.92:16410"
    LEN_HEAD = 4
    CACHE_INTERVAL = time.Second * 60
)

type Appid uint

type ReqStati struct {
    Op      string  `json:"op"`
    Appids  []Appid `json:"appids"`
    Topn    uint    `json:"topn"`
    Expand  string  `json:"expand"`
}

type RepStati struct {
    Op      string `json:"op"` 
    Expand  string `json:"expand"`
    Apps    []Rank `json:"apps"`
}

type Rank struct{
    Appid   uint            `json:"appid"`
    Sids    []RankDetail    `json:"sids"`
}

type RankDetail struct{
    Sid         uint    `json:"sid"`
    Usercount   uint    `json:"usercount"`
}

var mc *memcache.Client


func init() {
    mc = memcache.New(HOST_MEMCACHED)
}

func getAppids() []Appid {
    rep, _ := http.Get(URL_APPIDS)
    body, _ := ioutil.ReadAll(rep.Body)
    defer rep.Body.Close()

    var appids []Appid
    json.Unmarshal(body, &appids)    
    return appids
}


func getAppTopnSids() (rep RepStati) {
    conn, err := net.Dial("tcp", HOST_STATI)
    if err != nil {
        panic(err)
    }
    req := ReqStati{"batch_get_app_topn_sids", getAppids(), 12, ""} 
    jn, _ := json.Marshal(req)
    //head := make([]byte, LEN_HEAD)
    ////copy(head, string(len(jn)))
    //binary.LittleEndian.PutUint32(head, uint32(len(jn)))
    //msg := append(head, jn...)
    msg := make([]byte, len(jn) + LEN_HEAD)
    binary.LittleEndian.PutUint32(msg, uint32(len(jn)))
    copy(msg[LEN_HEAD:], jn)
    conn.Write(msg)

    var data bytes.Buffer
    //var rep RepStati
    buf := make([]byte, 2048)
    for {
        n, _ := conn.Read(buf)
        if n == 0 {
            break
        }
        data.Write(buf[:n])
        if data.Len() < LEN_HEAD {
            continue
        }
        len_msg := binary.LittleEndian.Uint32(data.Bytes()[:LEN_HEAD])
        if uint32(data.Len()) < len_msg + LEN_HEAD {
            continue
        }
        body := data.Bytes()[LEN_HEAD:len_msg+LEN_HEAD]
        json.Unmarshal(body, &rep)
        fmt.Println("result", rep.Apps)
        //return rep
        break
    }
    return
}

func cacheTopn() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("recovered")
        }
    }()
    ranks := getAppTopnSids().Apps
    var top1s  []Rank
    for _, rank := range ranks {
        appid := rank.Appid
        top12, _ := json.Marshal([]Rank{rank})
        top1 := Rank{appid, []RankDetail{rank.Sids[0]}}
        top1s = append(top1s, top1)
        mc.Set(&memcache.Item{Key:strconv.Itoa(int(appid)), Value:top12})
    }
    jn, _ := json.Marshal(top1s)
    mc.Set(&memcache.Item{Key:"top1s", Value:jn})

}


func main() {
    for {
        cacheTopn()
        time.Sleep(CACHE_INTERVAL)
    }
}

