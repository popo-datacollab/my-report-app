<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Data Analysis (Report 1-6)</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.2/papaparse.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f0f2f5; color: #333; }
        .container { max-width: 1400px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
        
        /* Layout Styling */
        h2 { text-align: center; color: #1a73e8; margin-top: 40px; padding-bottom: 10px; border-bottom: 3px solid #e8f0fe; }
        .upload-section { display: flex; gap: 15px; margin-bottom: 30px; justify-content: space-between; }
        .upload-box { flex: 1; border: 2px dashed #1a73e8; padding: 25px; text-align: center; border-radius: 12px; background: #f8fbff; cursor: pointer; transition: 0.3s; }
        .upload-box:hover { background: #eef4ff; border-color: #1557b0; }
        
        /* Table Styling (image_7b28db အတိုင်း) */
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; margin-bottom: 30px; border-radius: 8px; overflow: hidden; }
        th, td { border: 1px solid #dee2e6; padding: 12px 8px; text-align: center; }
        th { background-color: #1a73e8; color: white; font-weight: 600; }
        .sub-header { background-color: #e8f0fe; color: #1a73e8; font-weight: bold; }
        .grand-total-col { background-color: #d35400 !important; color: white !important; font-weight: bold; }
        .billing-group-col { background-color: #2e7d32 !important; color: white !important; font-weight: bold; }
        .tvie-col { background-color: #8e44ad !important; color: white !important; font-weight: bold; }

        /* Report 5 Card Styling */
        .report5-card { background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%); border-left: 8px solid #1a73e8; padding: 30px; text-align: center; margin: 20px 0; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .count-num { font-size: 4.5em; font-weight: 900; color: #1a73e8; margin: 0; line-height: 1; }
        
        /* Manual Search Section */
        .manual-input-section { background: #fafafa; padding: 25px; border: 1px solid #eee; border-radius: 12px; margin: 30px 0; }
        textarea { width: 100%; height: 100px; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 15px; box-sizing: border-box; }
        button { background-color: #1a73e8; color: white; border: none;
