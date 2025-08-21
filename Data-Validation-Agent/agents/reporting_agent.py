import json
from google.adk.agents import LlmAgent, tool
from config.settings import SUB_AGENT_MODEL, REPORTING_EMAIL_SENDER
from tools.reporting_tools import send_email_report, generate_pdf_report

class ReportingAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="ReportingAgent",
            description="Generates comprehensive reports from data validation results.",
            instruction="""You are a specialized agent for generating clear, concise, and actionable
                           reports from data validation results. Your task is to summarize discrepancies,
                           highlight critical issues, and provide an overview of data quality.
                           Format reports for easy consumption by various stakeholders. You can also
                           send reports via email or generate them in PDF format.""",
            tools=[send_email_report, generate_pdf_report] # Tools added here
        )

    @tool
    async def generate_report(self, validation_results: dict, recipients: list = None, format_type: str = "text") -> str:
        """
        Generates a summary report from the validation results and can optionally send it.
        In a real scenario, this could involve more complex LLM prompting for insights.

        Args:
            validation_results (dict): The output from the ValidationAgent.
            recipients (list, optional): A list of email addresses to send the report to. Defaults to None.
            format_type (str, optional): The desired format for the report ('text', 'pdf'). Defaults to 'text'.
        Returns:
            str: A natural language summary of the validation report.
        """
        print(f"Reporting Agent: Generating report for results: {validation_results}")

        overall_status = validation_results.get("summary", {}).get("overall_status", "UNKNOWN")
        total_discrepancies = validation_results.get("summary", {}).get("total_discrepancies", 0)
        detailed_results = validation_results.get("summary", {}).get("detailed_results",)

        report_lines = []
        report_lines.append(f"--- Data Validation Report ---")
        report_lines.append(f"Overall Status: {overall_status}")
        report_lines.append(f"Total Discrepancies Found: {total_discrepancies}")
        report_lines.append("\nDetailed Results:")

        if not detailed_results:
            report_lines.append("  No specific validation rules were run or no detailed results available.")
        else:
            for i, res in enumerate(detailed_results):
                rule_type = res.get("rule_type", "N/A")
                status = res.get("status", "UNKNOWN")
                details = res.get("details", {})
                report_lines.append(f"  Rule {i+1} ({rule_type}): Status - {status}")
                for key, value in details.items():
                    # Handle potential complex objects in details for better readability
                    if isinstance(value, (dict, list)):
                        report_lines.append(f"    {key}: {json.dumps(value, indent=2)}")
                    else:
                        report_lines.append(f"    {key}: {value}")
                report_lines.append("") # Add a blank line for readability

        final_report_content = "\n".join(report_lines)
        print("Reporting Agent: Report generated.")

        if recipients:
            subject = f"Data Validation Report - Status: {overall_status}"
            email_status = await self.tools.send_email_report(
                sender=REPORTING_EMAIL_SENDER,
                recipients=recipients,
                subject=subject,
                body=final_report_content
            )
            print(f"Reporting Agent: Email sending status: {email_status}")
            final_report_content += f"\n\nEmail notification sent: {email_status}"

        if format_type == "pdf":
            pdf_status = await self.tools.generate_pdf_report(
                report_content=final_report_content,
                file_name=f"data_validation_report_{overall_status}.pdf"
            )
            print(f"Reporting Agent: PDF generation status: {pdf_status}")
            final_report_content += f"\n\nPDF report generated: {pdf_status}"

        return final_report_content