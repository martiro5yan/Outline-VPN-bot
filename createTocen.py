from yoomoney import Authorize

Authorize(
      client_id="79BBEC4BB6A1C81B8FBB8EF402F26161E8FB1B5B35FA4AECBF075ABEC47B9F61",
      redirect_uri="https://vk.com/feed/",
      client_secret='41B9B6C603CABE0D4F0F998DA02B34158BF7F6B04CA44CC3D199F43C81A691325FC1CEC7F145732D0F9788941183F1C098A886510912EFFB74F2334973F6C4F9',
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )