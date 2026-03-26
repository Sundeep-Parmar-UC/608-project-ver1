# return sections of webpage as requested

def  htmlPagetemplate(section,UserMove = ""):

    Htmlsection = ""
    if section == 1:
        Htmlsection = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Chess Bot by Rita Group</title></head>'
        Htmlsection += '<body><div style="font-size: 16px; background-color: black; color: white; width: 100%; text-align: center;">'
        
        
        #define Header 
        Htmlsection += '<h3>Data 608:Chess Bot<br> by G5-Rita Group:  Michael, Sundeep, Yu Ling</h1>'
        Htmlsection += '<table style="font-size: 16px; background-color: black; color: white; margin: 0 auto; width: 50%; border-collapse: collapse; text-align: center;"><tbody><tr><td>'
        Htmlsection += '<table style="vertical-align: top;"><tbody>'
        
    elif section == 2:
        Htmlsection = """</tbody></table>
    </td><td style="vertical-align: top;">
<table style="vertical-align: top; font-size: 16px; width: 100%; max-width: 400px; border-collapse: collapse;">
  <thead>
    <tr style="background-color: black;">
      <th style="padding: 6px; border: 2px solid #ddd;">#</th>
      <th style="padding: 6px; border: 2px solid #ddd;">White</th>
      <th style="padding: 6px; border: 2px solid #ddd;">Black</th>
    </tr>
  </thead>
  <tbody>"""
    elif section == 25:
        Htmlsection = """ </tbody>
        </table>
        </td></tbody></table>	
        <hr>"""
        
    elif section == 3:
        Drop1a = "selected" if UserMove[0] == "a" else ""
        Drop1b = "selected" if UserMove[0] == "b" else ""
        Drop1c = "selected" if UserMove[0] == "c" else ""
        Drop1d = "selected" if UserMove[0] == "d" else ""
        Drop1e = "selected" if UserMove[0] == "e" else ""
        Drop1f = "selected" if UserMove[0] == "f" else ""
        Drop1g = "selected" if UserMove[0] == "g" else ""
        Drop1h = "selected" if UserMove[0] == "h" else ""
        Drop3a = "selected" if UserMove[2] == "a" else ""
        Drop3b = "selected" if UserMove[2] == "b" else ""
        Drop3c = "selected" if UserMove[2] == "c" else ""
        Drop3d = "selected" if UserMove[2] == "d" else ""
        Drop3e = "selected" if UserMove[2] == "e" else ""
        Drop3f = "selected" if UserMove[2] == "f" else ""
        Drop3g = "selected" if UserMove[2] == "g" else ""
        Drop3h = "selected" if UserMove[2] == "h" else ""
        Drop21 = "selected" if UserMove[1] == "1" else ""
        Drop22 = "selected" if UserMove[1] == "2" else ""
        Drop23 = "selected" if UserMove[1] == "3" else ""
        Drop24 = "selected" if UserMove[1] == "4" else ""
        Drop25 = "selected" if UserMove[1] == "5" else ""
        Drop26 = "selected" if UserMove[1] == "6" else ""
        Drop27 = "selected" if UserMove[1] == "7" else ""
        Drop28 = "selected" if UserMove[1] == "8" else ""
        Drop41 = "selected" if UserMove[3] == "1" else ""
        Drop42 = "selected" if UserMove[3] == "2" else ""
        Drop43 = "selected" if UserMove[3] == "3" else ""
        Drop44 = "selected" if UserMove[3] == "4" else ""
        Drop45 = "selected" if UserMove[3] == "5" else ""
        Drop46 = "selected" if UserMove[3] == "6" else ""
        Drop47 = "selected" if UserMove[3] == "7" else ""
        Drop48 = "selected" if UserMove[3] == "8" else ""
       
        Htmlsection = f"""
        	<form method="POST"><table style="font-size: 16px; background-color: black; color: white; margin: 0 auto; width: 50%; border-collapse: collapse; text-align: center;"><tbody><tr>
        	<td rowspan="2" colspan="2" style="font-size: 24px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;">Next Move:</td>
        	<td style="border: 2px solid #555;padding: 16px;">
        	Source Column </td>
        	<td style="border: 2px solid #555;padding: 16px;">
        	Source Row </td>
            <td style="border: 2px solid #555;padding: 16px;">
        	Destination Column </td>
            <td style="border: 2px solid #555;padding: 16px;">
        	Destination Row </td>
        		<td rowspan="2" style=" width: 200px; font-size: 24px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;"><button type="submit" name="action" value="calculate" style="font-size: 16px; background-color: black; color: gold; border: 2px solid gold; padding: 15px 30px; cursor: pointer; border-radius: 8px; font-weight: bold; margin: 20px auto; display: block;">
          Submit </button></td>
        	</tr><tr>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="SourceSpaceColoum" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">
        			<option value="a" {Drop1a}>A</option>
        			<option value="b" {Drop1b}>B</option>
        			<option value="c" {Drop1c}>C</option>
        			<option value="d" {Drop1d}>D</option>
        			<option value="e" {Drop1e}>E</option>
        			<option value="f" {Drop1f}>F</option>
        			<option value="g" {Drop1g}>G</option>
        			<option value="h" {Drop1h}>H</option>
        			</select>
        	</td>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="SourceSpaceRow" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">
        			<option value="1" {Drop21}>1</option>
        			<option value="2" {Drop22}>2</option>
        			<option value="3" {Drop23}>3</option>
        			<option value="4" {Drop24}>4</option>
        			<option value="5" {Drop25}>5</option>
        			<option value="6" {Drop26}>6</option>
        			<option value="7" {Drop27}>7</option>
        			<option value="8" {Drop28}>8</option>
        			</select>
        	</td>
        
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="DestinationSpaceColoum" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">
        			<option value="a" {Drop3a}>A</option>
        			<option value="b" {Drop3b}>B</option>
        			<option value="c" {Drop3c}>C</option>
        			<option value="d" {Drop3d}>D</option>
        			<option value="e" {Drop3e}>E</option>
        			<option value="f" {Drop3f}>F</option>
        			<option value="g" {Drop3g}>G</option>
        			<option value="h" {Drop3h}>H</option>
        			</select>
        	</td>
        	<td style="border: 2px solid #555;">
        		<select id="move-select" name="DestinationSpaceRow" style="font-size: 24px; padding-left: 20px; padding-right: 20px;">
        			<option value="1" {Drop41}>1</option>
        			<option value="2" {Drop42}>2</option>
        			<option value="3" {Drop43}>3</option>
        			<option value="4" {Drop44}>4</option>
        			<option value="5" {Drop45}>5</option>
        			<option value="6" {Drop46}>6</option>
        			<option value="7" {Drop47}>7</option>
        			<option value="8" {Drop48}>8</option>
        			</select>
        	</td>
        
        
        	</tr>"""
    elif section == 8:
        Htmlsection = """
        	<form method="POST"><table style="font-size: 16px; background-color: black; color: white; margin: 0 auto; width: 50%; border-collapse: collapse; text-align: center;"><tbody><tr>
        	<td colspan="5" style=" width: 300px; font-size: 24px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;">Created by G5-Rita Group: Michael, Sundeep, Yu Ling</td>
        	<td colspan="3" style="font-size: 24px;  border: 2px solid #555;  background-color: black; color: white;padding-left: 50px; padding-right: 50px;"><button type="submit" name="action" style="font-size: 16px; background-color: black; color: gold; border: 2px solid gold; padding: 15px 30px; cursor: pointer; border-radius: 8px; font-weight: bold; margin: 20px auto; display: block;" value="reset">
          Reset Game </button></td></tr>"""
    elif section == 4:
        Htmlsection = """</tbody></table></form>
        """
    elif section == 5:
        Htmlsection = """<BR><BR><BR><BR></div>
        	
        </body>
        </html>
        """

    return Htmlsection