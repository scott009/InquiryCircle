#!/usr/bin/env python3
"""
Add Vietnamese translations to Chapter 9 of rdg_en_v3.json
"""

import json
from pathlib import Path

# Vietnamese translations for Chapter 9
VIETNAMESE_TITLE = "PHỤC HỒI PHÁP LÀ GÌ?"

VIETNAMESE_PARAGRAPHS = {
    "p9-1": "Pháp là một từ Phạn ngữ có nghĩa là \"chân lý,\" \"hiện tượng,\" hoặc \"bản chất của sự vật.\" Khi viết hoa chữ cái đầu, Pháp thường có nghĩa là giáo pháp của Đức Phật và các pháp hành dựa trên những giáo pháp đó.",

    "p9-2": "Đức Phật biết rằng tất cả chúng sinh, ở một mức độ nào đó, đều phải đấu tranh với khát ái — ham muốn mạnh mẽ, đôi khi mù quáng để thay đổi suy nghĩ, cảm xúc, hoặc hoàn cảnh của chúng ta. Những người trong chúng ta trải qua nghiện ngập đã bị thúc đẩy sử dụng các chất gây nghiện và/hoặc hành vi có hại theo thói quen để cố gắng tạo ra sự thay đổi mong muốn này. Mặc dù Đức Phật không nói cụ thể về nghiện ngập, nhưng Ngài hiểu bản chất ám ảnh của tâm trí con người. Ngài hiểu sự gắn bó của chúng ta với khoái lạc và sự ghê sợ đau khổ. Ngài hiểu những biện pháp cực đoan mà chúng ta sẵn sàng thực hiện, đuổi theo những gì chúng ta muốn cảm nhận và chạy trốn khỏi những cảm giác chúng ta sợ hãi. Và Ngài đã tìm ra giải pháp.",

    "p9-3": "Cuốn sách này mô tả một cách để giải thoát chúng ta khỏi nỗi đau khổ của nghiện ngập bằng cách sử dụng các pháp hành và nguyên tắc Phật giáo. Chương trình này dẫn đến sự phục hồi từ nghiện các chất như rượu và ma túy và từ các nghiện quá trình như tình dục, cờ bạc, khiêu dâm, công nghệ, công việc, phụ thuộc lẫn nhau, mua sắm, ăn uống, truyền thông, tự gây tổn thương, nói dối, trộm cắp và lo lắng ám ảnh. Đây là con đường dẫn đến tự do khỏi bất kỳ hành vi lặp đi lặp lại và thói quen nào gây ra đau khổ.",

    "p9-4": "Một số người trong chúng ta đọc cuốn sách này có thể không quen thuộc với Phật giáo hoặc chưa sử dụng các pháp hành Phật giáo như một con đường phục hồi. Cũng có thể có những từ ngữ và khái niệm Phật giáo không quen thuộc trong cuốn sách này. Chúng tôi cũng hiểu rằng những gì chúng tôi trình bày trong cuốn sách này không bao gồm tất cả các truyền thống, dòng phái, giáo pháp và pháp hành Phật giáo, và có thể ở một mức độ nào đó khác với pháp hành Phật giáo của riêng bạn. Mục tiêu của chúng tôi là mô tả rõ ràng con đường và pháp hành của chúng tôi trong Phục Hồi Pháp cho những người mới phục hồi, mới với Phật giáo, và cho những người quen thuộc với cả hai. Cuốn sách này mô tả các giáo pháp Phật giáo nguyên thủy mà chương trình của chúng tôi xuất phát từ đó, bản chất của các giáo pháp căn bản và sơ kỳ của Phật giáo — Tứ Diệu Đế — để cho thấy cách thực hành Bát Chánh Đạo là một con đường thực dụng có thể chuyển hóa những thách thức của cả phục hồi sớm và lâu dài.",

    "p9-5": "Đây là một chương trình dựa trên sự từ bỏ. Bất kể nghiện ngập cá nhân của chúng ta là gì, tất cả các thành viên của chúng tôi cam kết kiêng cữ cơ bản từ chất hoặc hành vi đó. Đối với các nghiện quá trình như thức ăn và công nghệ, từ bỏ có thể có nghĩa là thiết lập ranh giới và ý định chu đáo. Đối với một số người trong chúng ta, kiêng cữ những thứ như hành vi tình dục ám ảnh, hoặc cưỡng ép tìm kiếm tình yêu và các mối quan hệ, có thể là cần thiết khi chúng ta làm việc để hiểu và tìm ranh giới có ý nghĩa. Nhiều người trong chúng ta đã phát hiện ra rằng sau khi từ bỏ nghiện chính của mình trong một khoảng thời gian, các hành vi có hại khác và các nghiện quá trình khác trở nên rõ ràng trong cuộc sống của chúng ta. Thay vì nản lòng, chúng tôi nhận thấy rằng chúng ta có thể gặp gỡ những hành vi này với lòng từ bi, trí tuệ và sự điều tra kiên nhẫn vào các xu hướng thói quen của chúng ta. Chúng tôi tin rằng phục hồi là một quá trình toàn diện suốt đời của việc lột bỏ các lớp thói quen và hành vi có điều kiện để tìm ra tiềm năng giác ngộ của chính chúng ta.",

    "p9-6": "Chương trình của chúng tôi do đồng đạo dẫn dắt: chúng tôi không theo bất kỳ giáo viên hoặc lãnh đạo nào. Chúng tôi hỗ trợ lẫn nhau như những đối tác cùng đi trên con đường phục hồi. Đây không phải là một chương trình dựa trên giáo điều hoặc tôn giáo, mà là tìm kiếm chân lý cho chính chúng ta. Sự hiểu biết này đã có tác dụng đối với chúng tôi, nhưng không phải là con đường duy nhất. Nó hoàn toàn tương thích với các con đường tâm linh và chương trình phục hồi khác. Chúng tôi biết từ kinh nghiệm của chính mình rằng phục hồi thực sự chỉ có thể thực hiện với ý định của sự trung thực triệt để, sự hiểu biết, nhận thức và chính trực, và chúng tôi tin tưởng bạn khám phá con đường của riêng bạn.",

    "p9-7": "Đây là một chương trình yêu cầu chúng ta không bao giờ ngừng phát triển. Nó yêu cầu chúng ta làm chủ các lựa chọn của mình và chịu trách nhiệm về sự chữa lành của chính mình. Nó dựa trên chánh niệm, lòng tốt, sự hào phóng, tha thứ và lòng từ bi sâu sắc.",

    "p9-8": "Chúng tôi không dựa vào các phương pháp xấu hổ và sợ hãi làm động lực. Những điều này đã không hiệu quả trong quá khứ của chúng ta, và thường tạo ra nhiều đấu tranh và đau khổ hơn thông qua tái nghiện và nản lòng. Sự can đảm cần thiết để phục hồi từ nghiện ngập cuối cùng là sự can đảm của trái tim, và chúng tôi hướng tới việc hỗ trợ lẫn nhau khi chúng ta cam kết với công việc dũng cảm này.",

    "p9-9": "Nhiều người trong chúng ta đã dành rất nhiều thời gian để phê bình bản thân. Trong chương trình này, chúng tôi từ bỏ bạo lực và gây hại, bao gồm cả bạo lực và tổn hại mà chúng ta gây ra cho chính mình. Chúng tôi tin vào sức mạnh chữa lành của sự tha thứ. Chúng tôi đặt niềm tin vào tiềm năng giác ngộ và phục hồi của chính mình, vào Tứ Diệu Đế của Đức Phật, và vào những người chúng ta gặp gỡ và kết nối trong các cuộc họp và trong suốt hành trình phục hồi của chúng ta.",

    "p9-10": "Tất nhiên chúng ta không thể thoát khỏi các hoàn cảnh và điều kiện là một phần của tình trạng con người. Chúng ta đã thử rồi — thông qua ma túy và rượu, thông qua tình dục và phụ thuộc lẫn nhau, thông qua cờ bạc và công nghệ, thông qua công việc và mua sắm, thông qua thức ăn hoặc hạn chế thức ăn, thông qua nỗi ám ảnh và những nỗ lực vô ích để kiểm soát trải nghiệm và cảm xúc của chúng ta — và chúng ta ở đây vì nó không hiệu quả. Đây là một chương trình mời gọi chúng ta nhận ra và chấp nhận rằng một số nỗi đau và thất vọng sẽ luôn hiện diện, để điều tra những cách không khéo léo mà chúng ta đã đối phó với nỗi đau đó trong quá khứ, và phát triển thói quen hiểu biết, lòng từ bi, tha thứ và nhận thức sâu sắc đối với nỗi đau của chính chúng ta, nỗi đau của người khác và nỗi đau mà chúng ta đã gây ra. Chấp nhận với nhận thức sâu sắc và lòng từ bi là những gì tạo ra tự do khỏi nỗi đau khổ khiến nỗi đau của chúng ta có vẻ không thể chịu đựng được.",

    "p9-11": "Cuốn sách này chỉ là phần giới thiệu về một con đường có thể mang lại giải thoát và tự do khỏi chu kỳ nghiện ngập. Ý định và hy vọng của chương trình chúng tôi là mỗi người trên con đường sẽ được trao quyền để biến nó thành của riêng mình.",

    "p9-12": "Cầu mong bạn được hạnh phúc.",

    "p9-13": "Cầu mong bạn được an lạc.",

    "p9-14": "Cầu mong bạn được giải thoát khỏi đau khổ.",

    "p9-15": "Cầu mong tất cả chúng sinh được giải thoát khỏi đau khổ."
}

def main():
    """Update JSON with Vietnamese translations for Chapter 9."""
    input_file = Path("/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/rdg_en_v3.json")

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create backup
    backup_file = input_file.with_name('rdg_en_v3.json.backup_before_vietnamese')
    print(f"Creating backup at {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Adding Vietnamese translations to Chapter 9...")

    # Find and update Chapter 9
    updated_count = 0
    for section in data['content']:
        if 'chapters' in section:
            for chapter in section['chapters']:
                if chapter.get('title') == 'WHAT IS RECOVERY DHARMA?':
                    # Add Vietnamese title
                    chapter['vietnamese_title'] = VIETNAMESE_TITLE
                    print(f"✓ Updated chapter title")

                    # Update paragraphs
                    for sec in chapter.get('sections', []):
                        for content_item in sec.get('content', []):
                            if content_item.get('type') == 'paragraph':
                                para_id = content_item['id']
                                if para_id in VIETNAMESE_PARAGRAPHS:
                                    content_item['vietnamese_text'] = VIETNAMESE_PARAGRAPHS[para_id]
                                    updated_count += 1
                                    print(f"✓ Updated {para_id}")

    print(f"\nSaving updated JSON...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Vietnamese translations added successfully!")
    print(f"   Updated: 1 title + {updated_count} paragraphs")
    print(f"   Backup saved at: {backup_file}")

if __name__ == "__main__":
    main()
