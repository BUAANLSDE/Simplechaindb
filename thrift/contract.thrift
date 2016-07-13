/**
 *  bool        Boolean, one byte
 *  i8 (byte)   Signed 8-bit integer
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 */


service Contract {
     bool creat_video(1: string video_hash, 2:double cost),
     bool transfer_video(1: string video_hash, 2:string owner_id, 3:string buyer_id),
     bool creat_coin(1:string user_id),
     bool transfer_coin(1:string owner_id, 2:string buyer_id)
}
