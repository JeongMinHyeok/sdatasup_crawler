def modify_df(df, index, crawl_list):
    if crawl_list[0] != df['ori공개일자'][index]:
        print(crawl_list[0], df['ori공개일자'][index])
        df['ori공개일자_변경여부'][index] = '1'
        df['up공개일자'][index] = crawl_list[0]
        pass
    else:
        df['up공개일자'][index] = crawl_list[0]
        pass
    
    if crawl_list[1] != df['ori최신수정일자'][index]:
        df['ori최신수정일자_변경여부'][index] = '1'
        df['up최신수정일자'][index] = crawl_list[1]
        pass
    else:
        df['up최신수정일자'][index] = crawl_list[1]
        pass
    
    if crawl_list[-1] != df['링크'][index]:
        df['기타사항'][index] = str(crawl_list[-1])
        
    return df