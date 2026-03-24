# return sections of webpage as requested

def  htmlPagetemplate(section):

    Htmlsection = ""
    if section == 1:
        Htmlsection = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Chess Bot by Rita Group</title></head>'
        Htmlsection += '<body><div style="font-size: 34px; background-color: black; color: white; width: 100%; text-align: center;">'
        
        
        #define Header 
        Htmlsection += '<h1><BIG>Welcome to Chess Bot </BIG></h1>'
        Htmlsection += '<table style="font-size: 24px; background-color: black; color: white; margin: 0 auto; width: 50%; border-collapse: collapse; text-align: center;"><tbody><tr><td>'
        Htmlsection += '<table style="vertical-align: top;"><tbody>'
        
    elif section == 2:
        Htmlsection = """</tbody></table>
    </td><td style="vertical-align: top;">
<table style="vertical-align: top; font-size: 24px; width: 100%; max-width: 400px; border-collapse: collapse;">
  <thead>
    <tr style="background-color: black;">
      <th style="padding: 6px; border: 2px solid #ddd;">#</th>
      <th style="padding: 6px; border: 2px solid #ddd;">White</th>
      <th style="padding: 6px; border: 2px solid #ddd;">Black</th>
    </tr>
  </thead>
  <tbody>"""

    elif section == 3:
        Htmlsection = """ </tbody>
        </table>
        </td></tbody></table>	
        <hr>
        	<form method="POST"><table style="font-size: 24px; background-color: black; color: white; margin: 0 auto; width: 50%; border-collapse: collapse; text-align: center;"><tbody><tr>
        	<td rowspan="2" style="font-size: 34px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;">Next Move:</td>
        	<td style="border: 2px solid #555;padding: 16px;">
        	Source Column </td>
        	<td style="border: 2px solid #555;padding: 16px;">
        	Source Row </td>
            <td style="border: 2px solid #555;padding: 16px;">
        	Destination Column </td>
            <td style="border: 2px solid #555;padding: 16px;">
        	Destination Row </td>
        		<td rowspan="2" style="font-size: 34px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;"><button type="submit" style="font-size: 24px; background-color: black; color: gold; border: 2px solid gold; padding: 15px 30px; cursor: pointer; border-radius: 8px; font-weight: bold; margin: 20px auto; display: block;">
          Submit
        </f></td>
        
        	</tr><tr>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="SourceSpaceColoum" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">
        			<option value="a">A</option>
        			<option value="b">B</option>
        			<option value="c">C</option>
        			<option value="d">D</option>
        			<option value="e">E</option>
        			<option value="f">F</option>
        			<option value="g">G</option>
        			<option value="h">H</option>
        			</select>
        	</td>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="SourceSpaceRow" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">
        			<option value="1">1</option>
        			<option value="2">2</option>
        			<option value="3">3</option>
        			<option value="4">4</option>
        			<option value="5">5</option>
        			<option value="6">6</option>
        			<option value="7">7</option>
        			<option value="8">8</option>
        			</select>
        	</td>
        
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="DestinationSpaceColoum" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">
        			<option value="a">A</option>
        			<option value="b">B</option>
        			<option value="c">C</option>
        			<option value="d">D</option>
        			<option value="e">E</option>
        			<option value="f">F</option>
        			<option value="g">G</option>
        			<option value="h">H</option>
        			</select>
        	</td>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="DestinationSpaceRow" style="font-size: 34px; padding-left: 20px; padding-right: 20px;">
        			<option value="1">1</option>
        			<option value="2">2</option>
        			<option value="3">3</option>
        			<option value="4">4</option>
        			<option value="5">5</option>
        			<option value="6">6</option>
        			<option value="7">7</option>
        			<option value="8">8</option>
        			</select>
        	</td>
        
        
        	</tr>"""
    elif section == 4:
        Htmlsection = """</tbody></table></form>
        <p style="color: red; font-style: italic;font-size: 24px;">
        """
    elif section == 5:
        Htmlsection = """</p><br><br><br><br></div>
        	
        </body>
        </html>
        """

        BotDifficulty = "1000"  #1000-Easy ,  1500 - Medium,  2500 - Hard,  5000 - Grandmaster
        MetricDisplay = "1"   #1 - display metrics   0 - do not display
        RemarkType = "first move"  #1) first move  2) general move  3)Black won 4) UniqueMovePosition 5)Illegal Move
        SnarkLevel = "neutral" #off, neutral, positive, evil


    
    return Htmlsection