import React from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import * as IoIcons from "react-icons/io";

export const SidebarData = [
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: <AiIcons.AiFillHome />,
    cName: "nav-text",
    roles: ["professor", "student"], // Accessible to all
  },
  {
    title: "Workspace",
    path: "/workspace",
    icon: <IoIcons.IoIosPaper />,
    cName: "nav-text",
    roles: ["professor", "student"], // Accessible to all
  },
  {
    title: "Courses",
    path: "/courses",
    icon: <FaIcons.FaCartPlus />,
    cName: "nav-text",
    roles: ["professor", "student"], // Accessible to all
  },
  {
    title: "Instructor Panel",
    path: "/instructor-panel",
    icon: <FaIcons.FaChalkboardTeacher />,
    cName: "nav-text",
    roles: ["professor"], // Accessible only to professors
  },
  {
    title: "Leaderboard",
    path: "/leaderboard",
    icon: <IoIcons.IoMdPeople />,
    cName: "nav-text",
    roles: ["student"], // Accessible only to students
  },
  {
    title: "Messages",
    path: "/messages",
    icon: <FaIcons.FaEnvelopeOpenText />,
    cName: "nav-text",
    roles: ["professor", "student"], // Accessible to all
  },
  {
    title: "Support",
    path: "/support",
    icon: <IoIcons.IoMdHelpCircle />,
    cName: "nav-text",
    roles: ["professor", "student"], // Accessible to all
  },
];