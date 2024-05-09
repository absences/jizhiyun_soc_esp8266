#ifndef GAGENT_SOC_H
#define GAGENT_SOC_H
#include "os_type.h"

#ifndef MCU_PROTOCOLVER_LEN
#define MCU_PROTOCOLVER_LEN 8
#define MCU_P0VER_LEN 8
#define MCU_HARDVER_LEN 8
#define MCU_SOFTVER_LEN 8
#define MCU_MCUATTR_LEN 8
#define PK_LEN       32
#define PK_SECRET_LEN 32
#endif
#define SDK_USER_VER_LEN        2

typedef void (*gagentConnectCb)(int32 result, uint8* pszDID, uint8 *szPasscode, void *arg);
typedef void (*gagentResetSimulatorCb)(int32 result, uint8* szMac, void *arg);
typedef void (*gagentUploadDataCb)( int32 result,void *arg,uint8* pszDID);
typedef void (*gagentDisconnectCb)(int32 result, uint8* pszDID, void *arg);
typedef void (*gagentAuthCb)( int32 result );

struct devAttrs
{
    unsigned short mBindEnableTime;
    unsigned char mstrProtocolVer[MCU_PROTOCOLVER_LEN];
    unsigned char mstrP0Ver[MCU_P0VER_LEN];
    unsigned char mstrDevHV[MCU_HARDVER_LEN];
    unsigned char mstrDevSV[MCU_SOFTVER_LEN];
    unsigned char mstrProductKey[PK_LEN];
    unsigned char mstrPKSecret[PK_SECRET_LEN];
    unsigned char mDevAttr[MCU_MCUATTR_LEN];
    unsigned char mstrSdkVerLow[SDK_USER_VER_LEN];
    gagentAuthCb  pUserStartFun;
    //gagent 微信公众号ID,默认为机智云微信宠物屋ID
    uint8 *szWechatDeviceType;
    //gagent 默认连接服务器域名
    uint8 *szGAgentSever;
    //gagent 默认连接服务器端口，默认为80
    uint32 *gagentSeverPort;
    //gagent softap Name ,默认值:XPG-GAgent-xxxx(后面4位为MAC后4位)
    uint8 *szGAgentSoftApName;
    uint8 *szGAgentSoftApName0;
    //gagent softap 密码 ,默认值:123456789，若内容为空则热点不加密;
    uint8 *szGAgentSoftApPwd;
    //m2m keepalive 默认值 120s
    uint32 *m2mKeepAliveS;
    //m2m 心跳间隔 默认值为 50s
    uint32 *m2mHeartbeatIntervalS;
    //gagent 时区秒，默认为东八区:8*(60*60)
    int32 *timeZoneS;
    //串口心跳间隔S，默认值 55秒
    uint32 *localHeartbeatIntervalS;
    //串口数据传送ACK时间，默认值600ms+数据长度耗时
    uint32 *localTransferIntervalMS;
    //网卡名称
    uint8 *networkCardName;
    // 默认配置模式,1:AP,2:airlink
    uint8 *configMode;
    //扫描次数
    uint8 *tScanNum;
    //是否直连路由
    uint8 *tCon;
};

typedef struct
{
   unsigned short year;
   unsigned char month;
   unsigned char day;
   unsigned char hour;
   unsigned char minute;
   unsigned char second;
   unsigned int ntp;
}_tm;

void gagentDisconnectM2M(uint8 *szDID, void *arg, gagentDisconnectCb fun);
void gagentProcessRun(os_event_t *events);
//连接云端获取DID
int32 gagentconnect2M2M(uint8 *szMac, uint8 *szPk, uint8 *szPks,uint8 *szDID, uint8 *szPasscode, int8 flag,void *arg,gagentConnectCb fun );
//接触该设备的用户绑定关系
int32 gagentResetSimulator( uint8 *szMac,uint8 *szPk, uint8 *szPks,uint8 *szPasscode, void *arg,gagentResetSimulatorCb fun );
//上传数据到app
int32 gagentUploadData(uint8 *szDID, uint8 *src, uint32 len,uint8 flag, void *arg,gagentUploadDataCb fun );
void gagentGetNTP(_tm *time);

/******************************************************
 *      FUNCTION        :   uGAgent_Config
 *      typed           :   1:AP MODE 2:Airlink
 *
 ********************************************************/
void gagentConfig(unsigned char configType);
void gagentReset(void);
void gagentInit(struct devAttrs attrs);
void gagentAuthInit( gagentAuthCb fun);
/**********************************************************
* @function GAgentEnableBind
* @brief    ÔÊÐíÓÃ»§°ó¶¨Éè±¸
**********************************************************/
void GAgentEnableBind();

#endif /* #endif GAGENT_EXTERNAL_H */

